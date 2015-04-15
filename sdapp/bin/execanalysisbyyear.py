from sdapp.models import SecurityPriceHist, ClosePrice, Form345Entry
from sdapp.models import YearlyReportingPersonAtts
import datetime
from decimal import Decimal
from django.db.models import Q
import django.db
import pytz

days_over_which_a_trade_is_evaluated = 180
trade_delta = datetime.timedelta(days_over_which_a_trade_is_evaluated)
win_hurdle = .10


def irrelevant():
    relevant = False
    return relevant, None, None, None, None, None, None, None, None


def laxer_start_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date+wkd_td)\
        .filter(close_date__gte=date + datetime.timedelta(1))\
        .order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_start(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date + datetime.timedelta(1))
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_start_price(sec_price_hist, date)


# Note that the date calculations are intentionally conservative measures
# of returns; start date is no LESS than filingdatetime + 1 and ending date
# is no MORE than filingdatetime + 1.  E.g. If you test over 7 days, you
# get the advantage of an avg effective period of over 7 days because you'll
# regularly have to grab the close price on Monday if t + 7 falls on a
# saturday.

def laxer_end_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date + datetime.timedelta(1))\
        .filter(close_date__gte=date - wkd_td + datetime.timedelta(2))\
        .order_by('-close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_end(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date + datetime.timedelta(1))
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_end_price(sec_price_hist, date)


def xnanalyze(repperson, filedate, acq_or_disp, issuer, trade_delta,
              win_hurdle):
    sec_price_hist_qs = SecurityPriceHist.objects.filter(issuer=issuer)
    # First figure out if the necessary information (ticker sym, necessary
    # price history exist)
    if sec_price_hist_qs.exists():
        sec_price_hist = sec_price_hist_qs[0]
    else:
        return irrelevant()
    # print 'repperson:', repperson,
    start_price = get_start(sec_price_hist, filedate)
    price_10 = get_end(sec_price_hist, filedate + datetime.timedelta(10))
    price_30 = get_end(sec_price_hist, filedate + datetime.timedelta(30))
    price_60 = get_end(sec_price_hist, filedate + datetime.timedelta(60))
    price_90 = get_end(sec_price_hist, filedate + datetime.timedelta(90))
    price_120 = get_end(sec_price_hist, filedate + datetime.timedelta(120))
    price_150 = get_end(sec_price_hist, filedate + datetime.timedelta(150))
    price_180 = get_end(sec_price_hist, filedate + datetime.timedelta(180))
    if start_price is None or price_180 is None:
        # print 'no start price'
        return irrelevant()
    # Note the below day calculation may not be perfect for all scenarios
    # because in some cases, a transaction may somehow happen on a day for
    # which we don't have a closing price.  We should generally be okay,
    # though.
    if start_price == 0:
        # print 'start price is zero'
        return irrelevant()
    perf_10 = ((price_10 - start_price) / start_price)
    perf_30 = ((price_30 - start_price) / start_price)
    perf_60 = ((price_60 - start_price) / start_price)
    perf_90 = ((price_90 - start_price) / start_price)
    perf_120 = ((price_120 - start_price) / start_price)
    perf_150 = ((price_150 - start_price) / start_price)
    perf_180 = ((price_180 - start_price) / start_price)
    # issuer_daily_perf = issuerdailyperf(sec_price_hist, repperson)
    # if issuer_daily_perf is None:
    # print 'no issuer daily perf'
    # return irrelevant()

    relevant = True
    # print 'went up'
    # print 'went down'
    success = False
    if perf_180 >= win_hurdle:
        success = True

    return (relevant, success, perf_10, perf_30, perf_60, perf_90,
            perf_120, perf_150, perf_180)


def execanalyze(qs, repperson, trade_delta, win_hurdle, start_dt, end_dt):
    execentries =\
        qs\
        .filter(reporting_owner_cik=repperson)
    buys = 0
    good_buys = 0

    exec_start =\
        Form345Entry.objects.filter(reporting_owner_cik=repperson)\
        .exclude(is_officer=False).earliest('filedatetime').filedatetime
    exec_end =\
        Form345Entry.objects.filter(reporting_owner_cik=repperson)\
        .exclude(is_officer=False).latest('filedatetime').filedatetime
    # Note that exec years is years as an SEC reporting exec
    exec_years = Decimal((exec_end - exec_start).days) / Decimal(365.25)
    gross_b_perf_10 = Decimal(0)
    gross_b_perf_30 = Decimal(0)
    gross_b_perf_60 = Decimal(0)
    gross_b_perf_90 = Decimal(0)
    gross_b_perf_120 = Decimal(0)
    gross_b_perf_150 = Decimal(0)
    gross_b_perf_180 = Decimal(0)
    # exexentrydates = execentries.datetimes('filedatetime', 'day').distinct()
    distinct_date_entries =\
        execentries.order_by('filedatetime', 'transaction_number')\
        .distinct('filedatetime')
    # for exexentrydate in exexentrydates:
    for firstentry in distinct_date_entries:
        filedate = firstentry.filedatetime.date()
        acq_or_disp = firstentry.xn_acq_disp_code
        issuer = firstentry.issuer_cik_num
        # Add weighting by units / value?
        (relevant, success, perf_10, perf_30, perf_60, perf_90, perf_120,
            perf_150, perf_180) = xnanalyze(repperson, filedate, acq_or_disp,
                                            issuer, trade_delta, win_hurdle)
        if relevant:
            buys += 1
            if success:
                good_buys += 1
            gross_b_perf_10 += perf_10
            gross_b_perf_30 += perf_30
            gross_b_perf_60 += perf_60
            gross_b_perf_90 += perf_90
            gross_b_perf_120 += perf_120
            gross_b_perf_150 += perf_150
            gross_b_perf_180 += perf_180

    if buys == 0:
        b_win_rate = None
        b_perf_10 = None
        b_perf_30 = None
        b_perf_60 = None
        b_perf_90 = None
        b_perf_120 = None
        b_perf_150 = None
        b_perf_180 = None
    else:
        b_win_rate = Decimal(good_buys) / Decimal(buys)

        b_perf_10 = gross_b_perf_10 / Decimal(buys)
        b_perf_30 = gross_b_perf_30 / Decimal(buys)
        b_perf_60 = gross_b_perf_60 / Decimal(buys)
        b_perf_90 = gross_b_perf_90 / Decimal(buys)
        b_perf_120 = gross_b_perf_120 / Decimal(buys)
        b_perf_150 = gross_b_perf_150 / Decimal(buys)
        b_perf_180 = gross_b_perf_180 / Decimal(buys)

    rpatts_object =\
        YearlyReportingPersonAtts(reporting_person_id=repperson,
                                  year=start_dt.year,
                                  buys=buys,
                                  b_win_rate_180=b_win_rate,
                                  exec_years=exec_years,
                                  b_perf_10=b_perf_10,
                                  b_perf_30=b_perf_30,
                                  b_perf_60=b_perf_60,
                                  b_perf_90=b_perf_90,
                                  b_perf_120=b_perf_120,
                                  b_perf_150=b_perf_150,
                                  b_perf_180=b_perf_180)  # .save()
    return rpatts_object


def reviewreppersons(qs, year, trade_delta):
    start_dt = datetime.datetime(year, 1, 1, tzinfo=pytz.utc)
    end_dt = datetime.datetime(year + 1, 1, 1, tzinfo=pytz.utc)
    print "Building YearlyReportingPersonAtts table..."
    '    Sorting, analyzing and saving...'
    yearqs =\
        qs\
        .filter(filedatetime__gte=start_dt)\
        .filter(filedatetime__lt=end_dt)
    reppersons =\
        yearqs\
        .values_list('reporting_owner_cik', flat=True).distinct()
    print '    Number of potential reporting persons:', len(reppersons)
    looplength = float(len(reppersons))
    counter = 0.0
    rpatts_objects = []
    for repperson in reppersons:
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print '   ', int(counter/looplength*100), 'percent'
        counter += 1.0
        rpatts_object = \
            execanalyze(yearqs, repperson, trade_delta, win_hurdle, start_dt,
                        end_dt)
        if rpatts_object is not None:
            rpatts_objects.append(rpatts_object)
    YearlyReportingPersonAtts.objects.bulk_create(rpatts_objects)
    django.db.reset_queries()
    print 'Done with this year'
    return


def reviewbyyear(trade_delta):
    YearlyReportingPersonAtts.objects.all().delete()
    execentries =\
        Form345Entry.objects\
        .filter(is_officer=True)\
        .exclude(transaction_date=None)\
        .filter(xn_acq_disp_code='A')\
        .filter(Q(transaction_code='P') |  # Open mkt / private purch
                Q(transaction_code='I'))  # Discretionary 16b-3 Xn

    execentrydates = execentries.datetimes('filedatetime', 'year').distinct()
    years = [x.year for x in execentrydates]
    for year in years:
        print "Reviewing ", year
        reviewreppersons(execentries, year, trade_delta)
    print 'Done'
    return

reviewbyyear(trade_delta)
