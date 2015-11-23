import datetime
from decimal import Decimal
import json
from math import sqrt
import pytz
import time

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

from sdapp.models import (SecurityPriceHist, ClosePrice,
                          Form345Entry)
from sdapp.bin.globals import today


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


def pull_person_holdings(ticker, issuer, person_cik, person_name,
                         firstpricedate):
    now = datetime.datetime.now(pytz.UTC)
    today = now.date()
    startdate = today - datetime.timedelta(270)
    startdt = now - datetime.timedelta(270)
    ticker_security =\
        SecurityPriceHist.objects.get(ticker_sym=ticker).security
    person_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .exclude(supersededdt__lte=startdt)\
        .filter(reporting_owner_cik=person_cik)
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

    all_values = person_forms\
        .filter(Q(security=ticker_security)
                | Q(underlying_security=ticker_security))\
        .exclude(reported_shares_following_xn=None)\
        .values_list('filedatetime', 'supersededdt',
                     'shares_following_xn', 'adjustment_factor',
                     'security__conversion_multiple')

    # print 'all_values', all_values
    # all_values = list(stock_values) + list(stock_deriv_values)
    date_set = set()
    for f, s, r, a, c in all_values:
        date_set.add(f)
        date_set.add(s)

    # for values in all_values:
    #     print values
    #     print ''

    xn_dict = {}
    for filedt, superseddt, rep_shares, adj_factor, conv_mult in all_values:
        if nd(filedt) in xn_dict:
            xn_dict[nd(filedt)] += Decimal(rep_shares) * Decimal(adj_factor)\
                * Decimal(conv_mult)
        else:
            xn_dict[nd(filedt)] = Decimal(rep_shares) * Decimal(adj_factor)\
                * Decimal(conv_mult)
        if nd(superseddt) in xn_dict:
            xn_dict[nd(superseddt)] -=\
                Decimal(rep_shares) * Decimal(adj_factor) * Decimal(conv_mult)
        else:
            xn_dict[nd(superseddt)] =\
                Decimal(-1) * Decimal(rep_shares) * Decimal(adj_factor)\
                * Decimal(conv_mult)

    if None in xn_dict:
        currentshares = Decimal(-1) * xn_dict.pop(None, None)
    else:
        currentshares = Decimal(0)
    person_data = []
    person_data = [[js_readable_date(datetime.date.today()), currentshares]]

    for key, value in sorted(xn_dict.iteritems(), reverse=True):
        if key >= startdate:
            person_data.append([js_readable_date(key), currentshares])
            currentshares -= xn_dict[key]
            person_data.append([js_readable_date(key), currentshares])
    # The below line appends the initial holdings at the startdate
    # for the closeprice graph
    # print person_data
    person_data.append([js_readable_date(firstpricedate), person_data[-1][1]])
    person_data = list(reversed(person_data))
    return person_data, person_name


def addholdingstograph(pl, ticker, issuer, persons_data, firstpricedate):
    graph = pl
    title_row = ['Date', 'Close Price']
    maxholding = 0
    print persons_data
    for person_cik, person_name in persons_data:
        # Builds adds empty row to right of price_json
        graph = [row + [None] for row in graph]
        # prices_json = map(list, zip(zip(*prices_json), rightemptylist))
        # calculates datelist, holdinglist for signal
        holding_data, person_name = \
            pull_person_holdings(ticker, issuer,
                                 person_cik, person_name, firstpricedate)

        # builds 'spacer' array of None entries to for new signal value column
        # spacer_length = len(datelist)
        title_row.append(person_name + ' Fully Diluted Shares')
        if len(graph) >= 2:
            spacer_width = len(graph[0]) - 2
        else:
            spacer_width = 1
        # spacer = [None] * len(prices_json[0]) - 2
        spaced_data = []
        for date, holding in holding_data:
            a = [None] * spacer_width
            a.insert(0, date)
            a.append(round(holding, 2))
            spaced_data.append(a)
            maxholding = max(maxholding, holding)
        graph += spaced_data

    return graph, title_row, maxholding


def buildgraphdata(issuer, ticker, persons_data):

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
    # if len(pricelist) > 0:
    #     firstpricedate = pricelist[0][0]
    # else:
    firstpricedate = datetime.date.today() - datetime.timedelta(270)

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
        addholdingstograph(pl, ticker, issuer, persons_data, firstpricedate)
    graph_json = json.dumps(list(graph), cls=DjangoJSONEncoder)
    titles_json = json.dumps(list(title_row), cls=DjangoJSONEncoder)
    ymax = Decimal(maxholding) * Decimal(1.30)
    return graph_json, titles_json, ymax
