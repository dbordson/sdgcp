from sdapp.models import CompanyStockHist
from django.db import connection
import requests
import datetime
# This requires requests, which can be installed via pip using "pip install
# requests" (http://docs.python-requests.org/en/latest/user/install/#install
# for info)

# Relevant Variables 
years = 1


def yahoodatetuple(dateobject):
    mindex = dateobject.month - 1
    dindex = dateobject.day
    yindex = dateobject.year

    return mindex, dindex, yindex


def csvscraper(url):
    # ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close',
    # 'Dividend/Special Distribution/Stock Split']

    IDprices = []
    response = requests.get(url)

    responsetext = response.text.encode('ascii')
    linelist = responsetext.rstrip().rsplit('\n')
    linelist.pop(0)
    for line in linelist:
        IDprices.append(line.rsplit(','))
    return IDprices


def tickerprices(entry):
    urlbase = 'http://ichart.yahoo.com/table.csv?s='
    ticker = entry.ticker_sym
    today = datetime.date.today()
    startday = datetime.date(today.year - years, today.month, today.day + 1)
    startdaytuple = yahoodatetuple(startday)
    todaytuple = yahoodatetuple(today)
    csvurl = urlbase + ticker + '&a=%s&b=%s&c=%s' % startdaytuple \
        + '&d=%s&e=%s&f=%s&g=d&ignore=.csv' % todaytuple
    tickerdata = csvscraper(csvurl)
    q = CompanyStockHist.objects.filter(ticker_sym=ticker)[0]
    for daydata in tickerdata:
        date = daydata[0]
        adjclose = daydata[6]
        q.closeprice_set.create(close_price=adjclose, close_date=date)
    q.save()
    return


def newstockprices():
    for entry in CompanyStockHist.objects.all():
        print entry
        tickerprices(entry)
    return


def update():
    print "beginning update..."
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE sdapp_closeprice")
    print "prior pricing data deleted"
    newstockprices()
    print "done"

update()
