from datetime import datetime, date
import sys

from pandas.io.data import DataReader

from sdapp.models import SecurityPriceHist, ClosePrice, SplitOrAdjustmentEvent


def savetickerinfo(SPH_id, ticker, security_id):
    yrs_of_pricing = 10
    yrs_of_adj = 10
    enddate = date.today()
    tickerdata =\
        DataReader(ticker, "yahoo", datetime(enddate.year-yrs_of_adj,
                                             enddate.month,
                                             enddate.day))
    tickerdata['Adj Factor'] =\
        tickerdata['Close'].divide(tickerdata['Adj Close'])

    tickerdata['Adj Factor Shifted'] =\
        tickerdata['Adj Factor'].shift(1)

    tickerdata['Adj Factor Old/New'] =\
        tickerdata['Adj Factor Shifted'].divide(tickerdata['Adj Factor'])

    # The data_to_cp does not need to exit if we are not limited on rows
    # to the extent we need past prices for the full period,
    # we may collapse these two calls into one DataFrame
    data_to_cp =\
        DataReader(ticker, "yahoo", datetime(enddate.year-yrs_of_pricing,
                                             enddate.month,
                                             enddate.day))
    data_to_cp['Adj Factor'] =\
        data_to_cp['Close'].divide(data_to_cp['Adj Close'])

    data_to_cp['Adj Factor Shifted'] =\
        data_to_cp['Adj Factor'].shift(1)

    data_to_cp['Adj Factor Old/New'] =\
        data_to_cp['Adj Factor Shifted'].divide(data_to_cp['Adj Factor'])

    ClosePrice.objects.filter(securitypricehist_id=SPH_id)\
        .delete()
    closepricesforsave = []
    for a in data_to_cp.itertuples():
        newcloseprice = ClosePrice(close_price=a[4],
                                   adj_close_price=a[6],
                                   close_date=str(datetime.date(a[0])),
                                   securitypricehist_id=SPH_id)
        closepricesforsave.append(newcloseprice)
    ClosePrice.objects.bulk_create(closepricesforsave)

    splitrecords = tickerdata.loc[tickerdata['Adj Factor Old/New'] >= 1.1]

    dictforsave = splitrecords.to_dict()['Adj Factor Old/New']

    for key in dictforsave:
        if not SplitOrAdjustmentEvent.objects.filter(security_id=security_id)\
                .filter(event_date=str(datetime.date(key)))\
                .exists():
                SplitOrAdjustmentEvent(
                    security_id=security_id,
                    adjustment_factor=round(dictforsave[key], 2),
                    event_date=str(datetime.date(key)))\
                    .save()

print "Updating stock price histories and split data...",
tickertuples = SecurityPriceHist.objects.values_list('id',
                                                     'ticker_sym',
                                                     'security')
counter = 0.0
looplength = float(len(tickertuples))
for SPH_id, ticker, security_id in tickertuples:
    try:
        savetickerinfo(SPH_id, ticker, security_id)
    except:
        print 'Error for:', SPH_id, ticker, security_id
    counter += 1.0
    percentcomplete = round(counter / looplength * 100, 2)
    sys.stdout.write("\r%s / %s tickers : %.2f%%" %
                     (int(counter), int(looplength), percentcomplete))
    sys.stdout.flush()
print "done."
