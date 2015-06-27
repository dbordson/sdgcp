import datetime
from decimal import Decimal
import json
from math import sqrt
import pytz
import time

from django.core.serializers.json import DjangoJSONEncoder

from sdapp.models import (SecurityPriceHist, Signal, ClosePrice,
                          Form345Entry)


def mean(lst):
    # """calculates mean"""
    lstsum = Decimal(0)
    for i in range(len(lst)):
        lstsum += lst[i]
    return (lstsum / len(lst))


def stddev(lst):
    # """calculates standard deviation"""
    lstsum = Decimal(0)
    mn = mean(lst)
    for entry in lst:
        lstsum += pow((entry - mn), 2)
    return sqrt(lstsum / Decimal(len(lst) - 1))


def js_readable_date(some_datetime_object):
    timetuple = some_datetime_object.timetuple()
    timestamp = time.mktime(timetuple)
    return timestamp * 1000.0


# converts date to datetime, but ignores None
def nd(dt):
    if isinstance(dt, datetime.datetime):
        return dt.date()

    elif dt is None:
        return dt
    else:
        print 'NEITHER DATETIME NOR NONE FED TO nd(dt) in holdingbuild.py'
        print 'dt ==', dt
        return dt


def pull_person_holdings(ticker, issuer, signal, firstpricedate):
    now = datetime.datetime.now(pytz.UTC)
    today = now.date()
    startdate = today - datetime.timedelta(270)

    ticker_security =\
        SecurityPriceHist.objects.get(ticker_sym=ticker).security
    person_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .exclude(supersededdt__lte=startdate)\
        .filter(reporting_owner_cik=signal.reporting_person)
    # The below pull is grabbing ticker holdings and derivatives
    # convertible directly into the ticker.
    # current_stock_holdings = person_forms.filter(supersededdt=None)\
    #     .filter(security=ticker_security)\
    #     .exclude(reported_shares_following_xn=None)
    # current_stock_values = current_stock_holdings\
    #     .values_list('filedatetime', 'supersededdt',
    #                  'reported_shares_following_xn', 'adjustment_factor')

    # current_stock_deriv_holdings = person_forms.filter(supersededdt=None)\
    #     .filter(underlying_security=ticker_security)\
    #     .exclude(underlying_shares=None)
    # current_stock_deriv_values = current_stock_deriv_holdings\
    #     .values_list('filedatetime', 'supersededdt',
    #                  'underlying_shares', 'adjustment_factor')
    # current_total =\
    #     dotproduct(current_stock_values)\
    #     + dotproduct(current_stock_deriv_values)

    date_set = set()
    stock_values = person_forms\
        .filter(security=ticker_security)\
        .exclude(reported_shares_following_xn=None)\
        .values_list('filedatetime', 'supersededdt',
                     'reported_shares_following_xn', 'adjustment_factor')

    stock_deriv_values = person_forms\
        .filter(underlying_security=ticker_security)\
        .exclude(underlying_shares=None)\
        .values_list('filedatetime', 'supersededdt',
                     'underlying_shares', 'adjustment_factor')

    all_values = list(stock_values) + list(stock_deriv_values)
    for f, s, r, a in all_values:
        date_set.add(f)
        date_set.add(s)
    # Don't use this because want to keep "None" values in dict
    # to represent current holdings
    # if None in date_set:
    #     date_set.remove(None)

    # date_list = list(date_set)

    xn_dict = {}
    for filedt, superseddt, rep_shares, adj_factor in all_values:
        if nd(filedt) in xn_dict:
            xn_dict[nd(filedt)] += Decimal(rep_shares) * Decimal(adj_factor)
        else:
            xn_dict[nd(filedt)] = Decimal(rep_shares) * Decimal(adj_factor)
        if nd(superseddt) in xn_dict:
            xn_dict[nd(superseddt)] -=\
                Decimal(rep_shares) * Decimal(adj_factor)
        else:
            xn_dict[nd(superseddt)] =\
                Decimal(-1) * Decimal(rep_shares) * Decimal(adj_factor)
    # print xn_dict
    if None in xn_dict:
        currentshares = Decimal(-1) * xn_dict.pop(None, None)
    else:
        currentshares = Decimal(0)
    signal_data = []
    signal_data = [[js_readable_date(datetime.date.today()), currentshares]]
    # print sorted(xn_dict.iteritems())
    for key, value in sorted(xn_dict.iteritems(), reverse=True):
        # print 'old', key, value
        if key >= startdate:
            signal_data.append([js_readable_date(key), currentshares])
            currentshares -= xn_dict[key]
            signal_data.append([js_readable_date(key), currentshares])
    # The below line appends the initial holdings at the startdate
    # for the closeprice graph
    signal_data.append([js_readable_date(firstpricedate), signal_data[-1][1]])
    signal_data = list(reversed(signal_data))
    return signal_data, signal.reporting_person_name


def addholdingstograph(pl, ticker, issuer, signals, firstpricedate):
    graph = pl
    title_row = ['Date', 'Close Price']
    maxholding = 0
    for signal in signals:
        # Builds adds empty row to right of price_json
        graph = [row + [None] for row in graph]
        # prices_json = map(list, zip(zip(*prices_json), rightemptylist))
        # calculates datelist, holdinglist for signal
        signal_data, signal_person_name = \
            pull_person_holdings(ticker, issuer, signal, firstpricedate)
        # builds 'spacer' array of None entries to for new signal value column
        # spacer_length = len(datelist)
        title_row.append(signal_person_name + ' Fully Diluted Shares')
        spacer_width = len(graph[0]) - 2
        # spacer = [None] * len(prices_json[0]) - 2
        spaced_data = []
        for date, holding in signal_data:
            # print date
            a = [None] * spacer_width
            a.insert(0, date)
            a.append(holding)
            spaced_data.append(a)
            maxholding = max(maxholding, holding)
        graph += spaced_data

    return graph, title_row, maxholding


def buildgraph(issuer, ticker):

    # Pulls signals and highlight dates of each signal
    signals = Signal.objects.filter(issuer=issuer)\
        .exclude(reporting_person=None)\
        .order_by('-signal_date')

    # Below grabs close prices
    SPH_objs = \
        SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(ticker_sym=ticker)
    if SPH_objs.exists():
        SPH_obj = SPH_objs[0]
    else:
        SPH_obj = None
    startdate = datetime.date.today() - datetime.timedelta(270)
    pricelist_qs = ClosePrice.objects.filter(securitypricehist=SPH_obj)\
        .filter(close_date__gte=startdate)\
        .order_by('close_date')
    pricelist = pricelist_qs\
        .values_list('close_date', 'adj_close_price')
    # standard deviation calculator, shows as shadding around line.
    firstpricedate = pricelist[0][0]

    # UNUSED CODE TO ADD STD DEVIATION FOR DYGRAPH ERROR BAR
    # [NOT STRAIGHTFORWARD TO WORK THESE BACK IN]
    # stddevlist = list(pricelist_qs.values_list('adj_close_price', flat=True))
    # standard_dev = round(float(stddev(stddevlist)), 2)

    # This builds the JSON price list
    pl = []
    # for close_date, adj_close_price in pricelist:
    #     pl.append([js_readable_date(close_date),
    #                [float(adj_close_price), float(standard_dev)]])

    for close_date, adj_close_price in pricelist:
        pl.append([js_readable_date(close_date),
                   float(adj_close_price)])

    graph, title_row, maxholding =\
        addholdingstograph(pl, ticker, issuer, signals, firstpricedate)
    graph_json = json.dumps(list(graph), cls=DjangoJSONEncoder)
    titles_json = json.dumps(list(title_row), cls=DjangoJSONEncoder)
    ymax = Decimal(maxholding) * Decimal(1.20)
    return graph_json, titles_json, ymax
