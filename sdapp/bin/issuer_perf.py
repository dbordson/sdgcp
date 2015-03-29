from sdapp.models import SecurityPriceHist, ClosePrice
from decimal import Decimal

all_issuers = \
    SecurityPriceHist.objects.all()\
    .values_list('issuer', flat=True).distinct()

print 'Starting'
ticker_returns = []
counter = 0
years_in_index = []
for issuer in all_issuers:
    sph_object = SecurityPriceHist.objects.filter(issuer=issuer)\
        .order_by('-ticker_sym')[0]
    print counter, sph_object.ticker_sym
    counter += 1
    CP_objects = \
        ClosePrice.objects.filter(securitypricehist=sph_object)\
        .order_by('close_date')
    if CP_objects.exists():
        first_price = CP_objects[0].adj_close_price
        last_price = list(CP_objects)[-1].adj_close_price
        first_date = CP_objects[0].close_date
        last_date = list(CP_objects)[-1].close_date
        years_diff = (last_date - first_date).days / Decimal(365.25)
        years_in_index.append(years_diff)
        ann_return =\
            (last_price / first_price)**(Decimal(1.0) / years_diff)\
            - Decimal(1.0)
        ticker_returns.append(ann_return)

simple_average_return = sum(ticker_returns) / len(ticker_returns)
print ''
print 'The simple average annual return for the tickers is',
print simple_average_return
avg_years = sum(years_in_index) / len(years_in_index)
print ''
print 'The average years in index for the tickers is',
print avg_years
