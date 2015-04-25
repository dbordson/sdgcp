from sdapp.models import Signal, Form345Entry  # , ClosePrice
import datetime
from django.db.models import F, Q
import pytz


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

Signal.objects.all().delete()
print 'Populating signals...'

today = datetime.datetime.now(pytz.utc)
lookback = datetime.timedelta(-90)

# insider discretionary buy
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
    # This builds the short statement to be displayed in the signal feed
    statement = '%s: the %s, %s, bought $%s of %s on a discretionary basis'\
        %\
        (str(entry.transaction_date),
         str(entry.reporting_owner_title),
         str(entry.reporting_owner_name),
         prep_num(int(entry.xn_price_per_share *
                      entry.transaction_shares)),
         str(entry.short_sec_title)
         )
    # This provides the significance of the statement.  I propose we only
    # include the signficance for the first discretionary buy displayed in the
    # signal feed (no need to repeat it over and over)
    significance = '; buys tend to foreshadow high stock performance.'
    new_signal = \
        Signal(issuer=entry.issuer_cik,
               security=entry.security,
               reporting_person=entry.reporting_owner_cik,
               reporting_person_name=entry.reporting_owner_name,
               reporting_person_title=entry.reporting_owner_title,
               signal_name='Discretionary Buy',
               signal_date=entry.filedatetime.date(),
               formentrysource=entry.entry_internal_id,
               security_title=entry.short_sec_title,
               security_units=entry.transaction_shares,
               signal_value=entry.xn_price_per_share *
               entry.transaction_shares,
               transactions=1,
               unit_conversion=entry.conversion_price,
               short_statement=statement,
               long_statement=statement+significance).save()

print '...Done'
