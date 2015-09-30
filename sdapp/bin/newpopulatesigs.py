import datetime
import pytz
from decimal import Decimal

import django.db
from django.db.models import F, Q

from sdapp.models import DiscretionaryXnEvent, Form345Entry, PersonSignal,\
    SecurityPriceHist, ClosePrice
from sdapp.models import WatchedName
from sdapp.bin.globals import lookback, weakness_drop,\
    abs_significance_minimum, rel_significance_minimum


def calc_holdings(securities, issuer):
    first_filing_date = securities[0][3]
    ticker_security =\
        SecurityPriceHist.objects.filter(issuer=issuer)[0].security
    person_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_person)\
        .exclude(supersededdt__lt=first_filing_date - datetime.timedelta(1))\
        .exclude(filedatetime__gte=first_filing_date - datetime.timedelta(1))
    stock_values = person_forms\
        .filter(security=ticker_security)\
        .exclude(reported_shares_following_xn=None)\
        .values_list('reported_shares_following_xn', 'adjustment_factor')
    stock_deriv_values = person_forms\
        .filter(underlying_security=ticker_security)\
        .exclude(underlying_shares=None)\
        .values_list('underlying_shares', 'adjustment_factor')
    all_values = list(stock_values) + list(stock_deriv_values)
    prior_holding_value = Decimal(0)
    for rep_shares, adj_factor in all_values:
        prior_holding_value += Decimal(rep_shares) * Decimal(adj_factor)

    return prior_holding_value

print 'Populating signals...'

today = datetime.datetime.now(pytz.utc)


# insider discretionary buy
print 'Discretionary Transactions'
print '    sorting...'
# screens recent buys

existing_sig_pks = DiscretionaryXnEvent.objects.values_list('form_entry__pk')

# Note that the below contains an 'F Object'; since this may be unfamiliar,
# I will explain -- it filters for transaction dates that are greater than
# 5 days (timedelta) before the filedatetime.  This avoids interpreting an old
# transaction in a newly filed form as a new signal.

a =\
    Form345Entry.objects\
    .filter(filedatetime__gte=today + lookback)\
    .filter(transaction_date__gte=F('filedatetime')
            + datetime.timedelta(-5))\
    .exclude(transaction_date=None)\
    .exclude(xn_price_per_share=None)\
    .exclude(transaction_shares=None)\
    .exclude(xn_acq_disp_code=None)\
    .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
    .exclude(pk__in=existing_sig_pks)
newxns = []
print '    interpreting and saving...'
for item in a:
    if item.xn_acq_disp_code == 'D':
        sign_transaction_shares = Decimal(-1) * item.transaction_shares
    else:
        sign_transaction_shares = item.transaction_shares
    xn_val = item.xn_price_per_share * sign_transaction_shares
    newxn =\
        DiscretionaryXnEvent(issuer=item.issuer_cik,
                             reporting_person=item.reporting_owner_cik,
                             security=item.security,
                             form_entry=item.pk,
                             xn_acq_disp_code=item.xn_acq_disp_code,
                             transaction_code=item.transaction_code,
                             xn_val=xn_val,
                             xn_shares=sign_transaction_shares,
                             filedate=item.filedatetime.date)
    newxns.append(newxn)
print '    saving...'
DiscretionaryXnEvent.objects.bulk_create(newxns)

print 'done.'
django.db.reset_queries()
print ''


print 'PersonSignal objects'

a =\
    DiscretionaryXnEvent.objects\
    .values_list('reporting_person', 'issuer').distinct()
newpersonsignals = []
for reporting_person, issuer in a:
    # When primary ticker concept is added, adjust filter accordingly.
    aff_events = DiscretionaryXnEvent.objects.filter(issuer=issuer)\
        .filter(reporting_person=reporting_person)
    sph = SecurityPriceHist.objects.filter(issuer=issuer)\
        .order_by('security__short_sec_title')[0]
    reporting_person_title = \
        Form345Entry.objects.filter(reporting_owner_cik=reporting_person)\
        .filter(filedatetime__gte=today + lookback)\
        .latest('filedatetime').person_title

    securities = aff_events.order_by('filedate')\
        .values_list('security', 'xn_val', 'xn_shares', 'filedate')

    entryfiledates = aff_events.order_by('filedate')\
        .order_by('filedatetime').values_list('filedatetime', flat=True)
    first_file_date = entryfiledates[0].date()
    last_file_date = entryfiledates[-1].date()
    transactions = len(entryfiledates)

    # Get holdings before form filed
    prior_holding_value = calc_holdings(securities, issuer)
    securities_dict = {}
    net_signal_value = Decimal(0)
    gross_acq_value = Decimal(0)
    gross_disp_value = Decimal(0)
    for security, xn_val, xn_shares, filedate in securities:
        if security in securities_dict:
            securities_dict[security][0] += xn_val
            securities_dict[security][1] += xn_shares

        else:
            securities_dict[security] = [xn_val. xn_shares]
        net_signal_value += xn_val
        if xn_val > 0:
            gross_acq_value += xn_val
        else:
            gross_disp_value += xn_val
    if gross_acq_value >= Decimal(-1) * gross_disp_value:
        gross_signal_value = gross_acq_value
    else:
        gross_signal_value = gross_disp_value
    security_1 = max(securities_dict, key=securities_dict.get)
    average_price_security_1 =\
        securities_dict[security_1][0] / securities_dict[security_1][1]
    net_signal_pct = net_signal_value / gross_signal_value * Decimal(100)
    if len(securities_dict) == 1:
        only_security_1 = True
    else:
        only_security_1 = False

    newpersonsignals.append(
        PersonSignal(issuer=issuer,
                     sph=sph,
                     reporting_person=reporting_person,
                     security_1=security_1,
                     only_security_1=only_security_1,
                     reporting_person_title=reporting_person_title,
                     signal_name=signal_name,
                     signal_detect_date=signal_detect_date,
                     first_file_date=first_file_date,
                     last_file_date=last_file_date,
                     transactions=transactions,
                     average_price_security_1=average_price_security_1,
                     gross_signal_value=gross_signal_value,
                     net_signal_value=net_signal_value,
                     prior_holding_value=prior_holding_value,
                     net_signal_pct=net_signal_pct,
                     preceding_stock_perf=preceding_stock_perf,
                     preceding_stock_period_days=preceding_stock_period_days,
                     ))


PersonSignal.objects.all().delete()
newpersonsignals.objects.bulk_create(newpersonsignals)
