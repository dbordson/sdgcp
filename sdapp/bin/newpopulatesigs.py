import datetime
import pytz
from decimal import Decimal

from django.db.models import F, Q

from sdapp.models import DiscretionaryXnEvent, Form345Entry,
    SecurityPriceHist, ClosePrice
from sdapp.models import WatchedName
from sdapp.bin.globals import *

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
newsignals = []
print '    interpreting and saving...'
for item in a:
    xn_val = entry.xn_price_per_share * entry.transaction_shares
    newsignal =\
        DiscretionaryXnEvent(issuer=item.issuer_cik,
                             reporting_person=item.reporting_owner_cik,
                             security=item.security,
                             form_entry=item.pk,
                             xn_acq_disp_code=item.xn_acq_disp_code,
                             transaction_code=item.transaction_code,
                             xn_val=xn_val,
                             filedate=item.filedatetime.date)
    newsignals.append(newsignal)
