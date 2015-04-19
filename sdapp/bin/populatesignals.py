from sdapp.models import Signal, Form345Entry, ClosePrice
import datetime


Signal.objects.all().delete()

today = datetime.date.today()
lookback = datetime.timedelta(-90)

# insider discretionary buy
a =\
    Form345Entry.objects\
    .filter(filedatetime__gte=today + lookback)\
    .filter(is_officer=True)\
    .exclude(transaction_date=None)\
    .filter(xn_acq_disp_code='A')\
    .filter(Q(transaction_code='P') |  # Open mkt / private purch
            Q(transaction_code='I'))  # Discretionary 16b-3 Xn

for entry in a:
    statement = ''
    new_signal = \
        Signal(issuer=entry.issuer_cik,
               security=entry.security,
               reporting_person=entry.reporting_owner_cik,
               signal_name='Discretionary Buy',
               signal_date=entry.filedatetime.date(),
               formentrysource=entry.entry_internal_id,
               security_units=entry.transaction_shares,
               signal_value=entry.xn_price_per_share *
               entry.transaction_shares,
               transactions=1,
               unit_conversion=entry.conversion_price,
               statement=
               )
