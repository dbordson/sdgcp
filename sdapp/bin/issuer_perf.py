from sdapp.models import SecurityPriceHist, ClosePrice
from decimal import Decimal
import datetime

all_issuers = \
    SecurityPriceHist.objects.all()\
    .values_list('issuer', flat=True).distinct()

print 'Starting calculation of average returns of available issuers'
ticker_returns = []
counter = 0
years_in_index = []
for issuer in all_issuers:
    sph_object = SecurityPriceHist.objects.filter(issuer=issuer)\
        .order_by('-ticker_sym')[0]
    # print counter, sph_object.ticker_sym
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
print round(float(simple_average_return) * 100.0, 2), ' percent'
avg_years = round(float(sum(years_in_index) / len(years_in_index)), 2)
print 'The average years in index for the tickers is',
print avg_years

print 'Starting calculation of annual returns of available issuers by year.'
thisyear = datetime.date.today().year
years = []
for x in range(0, 11):
    years.append(thisyear - x)
for year in years:
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year + 1, 1, 1)
    ticker_returns = []
    counter = 0
    years_in_index = []
    for issuer in all_issuers:
        sph_object = SecurityPriceHist.objects.filter(issuer=issuer)\
            .order_by('-ticker_sym')[0]
        # print counter, sph_object.ticker_sym
        counter += 1
        CP_objects = \
            ClosePrice.objects.filter(securitypricehist=sph_object)\
            .filter(close_date__lte=end_date)\
            .filter(close_date__gte=start_date)\
            .order_by('close_date')
        if CP_objects.exists():
            first_price = CP_objects[0].adj_close_price
            # print 'first_price', first_price,
            last_price = list(CP_objects)[-1].adj_close_price
            # print 'last_price', last_price,
            first_date = CP_objects[0].close_date
            # print 'first_date', first_date,
            last_date = list(CP_objects)[-1].close_date
            # print 'last_date', last_date,
            years_diff = Decimal((last_date - first_date).days) /\
                Decimal((end_date - start_date).days)
            # print 'years_diff', years_diff
            years_in_index.append(years_diff)
            name_return =\
                (last_price / first_price) - Decimal(1.0)
            # print 'ann_return', ann_return
            ticker_returns.append(name_return)

    # print ticker_returns
    # print 'sum(ticker_returns)', sum(ticker_returns)
    # print 'len(ticker_returns', len(ticker_returns)
    simple_average_return = sum(ticker_returns) / sum(years_in_index)
    print ''
    print 'The simple average return for the tickers in', year, 'is',
    print round(float(simple_average_return) * 100.0, 2), ' percent'
    avg_years = round(float(sum(years_in_index) / len(years_in_index)), 2)
    print 'The average years in index for the tickers is',
    print avg_years
