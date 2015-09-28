import datetime
import pytz
from decimal import Decimal

import django.db
from django.db.models import Count, F, Q, Max

from sdapp.models import DiscretionaryXnEvent, Form345Entry, PersonSignal,\
    SecurityPriceHist, ClosePrice
from sdapp.models import WatchedName
from sdapp.bin.globals import lookback, weakness_drop

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
    xn_val = item.xn_price_per_share * item.transaction_shares
    newxn =\
        DiscretionaryXnEvent(issuer=item.issuer_cik,
                             reporting_person=item.reporting_owner_cik,
                             security=item.security,
                             form_entry=item.pk,
                             xn_acq_disp_code=item.xn_acq_disp_code,
                             transaction_code=item.transaction_code,
                             xn_val=xn_val,
                             xn_shares=item.transaction_shares,
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
    xnmatrix = aff_events\
        .values_list('filedate', 'security', 'xn_acq_disp_code', 'xn_val',
                     'xn_shares')

    securities = aff_events.values_list('security', 'xn_val')
    securities_dict = {}
    for security, xn_val in securities:
        if security in securities_dict:
            securities_dict[security] += xn_val
        else:
            securities_dict[security] = xn_val
    security_1 = max(securities_dict, key=securities_dict.get)
    # ADD NET VALUE TO DICT ABOVE
    if len(securities_dict) == 1:
        only_security_1 = True
    else:
        only_security_1 = False

    transaction_dates = aff_events.order_by('filedate')\
        .order_by('filedatetime').values_list('filedatetime', flat=True)
    first_xn_date = transaction_dates[0].date()
    last_xn_date = transaction_dates[-1].date()
    transactions = len(transaction_dates)


    newpersonsignals.append(
        PersonSignal(issuer=issuer,
                     sph=sph,
                     reporting_person=reporting_person,
                     security_1=security_1,
                     only_security_1=only_security_1,
                     reporting_person_title=reporting_person_title,
                     signal_name=signal_name,
                     signal_detect_date=signal_detect_date,
                     first_xn_date=first_xn_date,
                     last_xn_date=last_xn_date,
                     transactions=transactions,
                     average_price=average_price,
                     gross_signal_value=gross_signal_value,
                     net_signal_value=net_signal_value,
                     end_holding_value=end_holding_value,
                     net_signal_pct=net_signal_pct,
                     preceding_stock_perf=preceding_stock_perf,
                     preceding_stock_period_days=preceding_stock_period_days,
                     ))


PersonSignal.objects.all().delete()
newpersonsignals.objects.bulk_create(newpersonsignals)
