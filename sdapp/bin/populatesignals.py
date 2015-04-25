from sdapp.models import Signal, Form345Entry, SecurityPriceHist, ClosePrice
import datetime
from django.db.models import F, Q
import pytz
from decimal import Decimal


def prep_num(a):
    float_a = float(a)
    # This rounds to the lesser of 2 sig figs and zero decimal places
    round_amount = min(-len(str(int(a))) + 2, 0)
    rounded_a = round(float_a, round_amount)
    # This adds the thousands separator
    formatted_a = format(int(rounded_a), ',d')
    if formatted_a == '0':
        print 'ERROR -- zero value transaction caught: ', a
        return None
    return formatted_a


def laxer_start_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date+wkd_td)\
        .filter(close_date__gte=date + datetime.timedelta(1))\
        .order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_start(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date + datetime.timedelta(1))
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_start_price(sec_price_hist, date)


def buy_signal_type(entry, sph, declinethreshhold, sig_name_db, sig_name_wb):
    filedate = entry.filedatetime.date()
    prior_price = get_start(sph, filedate +
                            datetime.timedelta(-90))
    filing_price = get_start(sph, filedate)
    decline = Decimal(-1) * (filing_price - prior_price) / prior_price
    decline_pct = str(int(decline * Decimal(100)))
    if decline > declinethreshhold:
        signal_name = sig_name_wb
        statement =\
            ('The %s, %s, bought $%s of %s after a %s percent price drop '
             + 'over six months')\
            %\
            (str(entry.reporting_owner_title),
             str(entry.reporting_owner_name),
             prep_num(int(entry.xn_price_per_share *
                          entry.transaction_shares)),
             str(entry.short_sec_title),
             str(decline_pct)
             )
        significance = '; this suggests a price below fundamental value.'
    else:
        signal_name = sig_name_db
        # This builds the short statement to be displayed in the signal feed
        statement =\
            'The %s, %s, bought $%s of %s on a discretionary basis'\
            %\
            (str(entry.reporting_owner_title),
             str(entry.reporting_owner_name),
             prep_num(int(entry.xn_price_per_share *
                          entry.transaction_shares)),
             str(entry.short_sec_title)
             )
        # This provides the significance of the statement.  I propose we only
        # include the signficance for the first discretionary buy displayed in
        # the signal feed (no need to repeat it over and over)
        significance = '; buys tend to foreshadow high stock performance.'
    return signal_name, statement, significance

Signal.objects.all().delete()
print 'Populating signals...'

today = datetime.datetime.now(pytz.utc)
lookback = datetime.timedelta(-90)

# insider discretionary buy
print 'Discretionary Buys'
print '    sorting...'
# screens recent buys
# Note that the below contains an 'F Object'; since this may be unfamiliar,
# I will explain -- it filters for transaction dates that are greater than
# 5 days (timedelta) before the filedatetime.  This avoids interpreting an old
# transaction in a newly filed form as a new signal.
a =\
    Form345Entry.objects\
    .filter(filedatetime__gte=today + lookback)\
    .filter(transaction_date__gte=F('filedatetime')
            + datetime.timedelta(-5))\
    .filter(is_officer=True)\
    .exclude(transaction_date=None)\
    .filter(xn_acq_disp_code='A')\
    .filter(Q(transaction_code='P') |  # Open mkt / private purch
            Q(transaction_code='I'))  # Discretionary 16b-3 Xn

print '    interpreting and saving...'
print '    discretionary buys...'
for entry in a:
    signal_name_db = 'Discretionary Buy'
    signal_name_wb = 'Discretionary Buy after a Decline'
    # Finds stock ticker
    sph_set = SecurityPriceHist.objects.filter(issuer=entry.issuer_cik)
    if sph_set.exists():
        sph = sph_set[0]
    else:
        pass
    signalmatch =\
        Signal.objects.filter(signal_date=entry.filedatetime.date())\
        .filter(issuer=entry.issuer_cik)\
        .filter(security=entry.security)\
        .filter(reporting_person=entry.reporting_owner_cik)\
        .filter(Q(signal_name=signal_name_db) |
                Q(signal_name=signal_name_wb))
    # print signalmatch.exists()
    # print signalmatch
    transactions = 1
    value = entry.xn_price_per_share * entry.transaction_shares
    # The below script checks to see if the signal here has already been
    # found and if so, extracts important information and deletes the old
    # in preparation of creating a new, updated signal.
    if signalmatch.exists():
        signal = signalmatch[0]
        # print signal.signal_value
        # print entry.xn_price_per_share *\
        #     entry.transaction_shares
        entry.transaction_shares += signal.security_units
        value += signal.signal_value
        transactions += signal.transactions
        signal.delete()
    dec = Decimal(.1)
    # assigns discretionary buy signal type
    signal_name, statement, significance =\
        buy_signal_type(entry, sph, dec, signal_name_db, signal_name_wb)

    new_signal = \
        Signal(issuer=entry.issuer_cik,
               security=entry.security,
               sph=sph,
               reporting_person=entry.reporting_owner_cik,
               reporting_person_name=entry.reporting_owner_name,
               reporting_person_title=entry.reporting_owner_title,
               signal_name=signal_name,
               signal_date=entry.filedatetime.date(),
               formentrysource=entry.entry_internal_id,
               security_title=entry.short_sec_title,
               security_units=entry.transaction_shares,
               signal_value=value,
               transactions=transactions,
               unit_conversion=entry.conversion_price,
               short_statement=statement,
               long_statement=statement+significance).save()

print '...Done'
