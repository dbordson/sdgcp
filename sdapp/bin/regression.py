from sdapp.models import Form345Entry, ClosePrice, Security, SecurityPriceHist
import pandas

a = Form345Entry.objects\
    .exclude(transaction_shares=None)\
    .exclude(transaction_date=None)\
    .values_list('issuer_cik',
                 'security',
                 'affiliation',
                 'transaction_shares',
                 'transaction_date')

issuers =\
    ClosePrice.objects.values_list('securitypricehist__issuer', flat=True)\
    .distinct()
dCPs = {}
for issuer in issuers:
    dCPs[issuer] = {}
    CPs = ClosePrice.objects\
        .filter(securitypricehist__issuer=issuer)\
        .values('close_date',
                'adj_close_price')
    for CP in CPs:
        dCPs[issuer][CP['close_date']] = CP['adj_close_price']


newa = []
for item in a:
    issuer = item[0]
    close_date = item[4]
    try:
        adj_close_price = dCPs[issuer][close_date]
    except:
        adj_close_price = None
    listrow = list(item)
    listrow.append(adj_close_price)
    newa.append(listrow)
a = newa

b = zip(*a)
d = {'issuer_cik': list(b[0]),
     'security': list(b[1]),
     'affiliation': list(b[2]),
     'transaction_shares': list(b[3]),
     'transaction_date': pandas.to_datetime(pandas.Series(list(b[4]))),
     'adj_close_price': list(b[5])}
transaction_data = pandas.DataFrame(d)\
    .sort('transaction_date', ascending=False)

