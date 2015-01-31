from sdapp.models import Form345Entry
import pandas

a = Form345Entry.objects\
    .exclude(transaction_shares=None)\
    .exclude(transaction_date=None)\
    .values_list('issuer_cik',
                 'affiliation',
                 'transaction_shares',
                 'transaction_date')
b = zip(*a)
d = {'issuer_cik': list(b[0]),
     'affiliation': list(b[1]),
     'transaction_shares': list(b[2]),
     'transaction_date': list(b[3])}
transaction_data = pandas.DataFrame(d)
