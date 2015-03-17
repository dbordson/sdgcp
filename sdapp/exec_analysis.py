from sdapp.models import SecurityPriceHist, ClosePrice, Form345Entry
from sdapp.models import ReportingPersonAtts
import datetime
from decimal import Decimal
from django.db.models import Q

days_over_which_a_trade_is_evaluated = 180
trade_delta = datetime.timedelta(days_over_which_a_trade_is_evaluated)


def irrelevant():
    relevant = 0
    success_or_failure = 0
    return relevant, success_or_failure


def get_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date)\
        .filter(close_date__gt=date-wkd_td).order_by('-close_prices')
    if price_list.exists():
        return price_list[0]
    else:
        return None


def issuerdailyperf(sec_price_hist, repperson):
    # Tries to calculate return over the period that the holder has
    # transacted in company stock.  Returns None if pricing unavailable
    # or less than a year of history.
    issuer = sec_price_hist.issuer
    entry_dates = \
        list(Form345Entry.objects
             .filter(issuer_cik=issuer, reporting_owner_cik=repperson)
             .order_by('filedatetime')
             .values_list('filedatetime', flat=True).distinct())
    first_date = entry_dates[0].date()
    last_date = entry_dates[-1].date()
    days = Decimal(((last_date - first_date).days))
    if days < 365.25:
        return None
    first_price = get_price(sec_price_hist, first_date)
    last_price = get_price(sec_price_hist, last_date)
    if first_price is None or last_price is None:
        return None
    daily_return = ((last_price - first_price) / first_price) / days

    return daily_return


def xnanalyze(repperson, xndate, acq_or_disp, issuer, trade_delta):
    sec_price_hist_qs = SecurityPriceHist.objects.filter(issuer_pk=issuer)
    # First figure out if the necessary information (ticker sym, necessary
    # price history exist)
    if sec_price_hist_qs.exists():
        sec_price_hist = sec_price_hist_qs[0]
    else:
        return irrelevant()

    start_price = get_price(sec_price_hist, xndate)
    enddate = xndate + trade_delta
    end_price = get_price(sec_price_hist, enddate)
    if start_price is None or end_price is None:
        return irrelevant()
    # Note the below day calculation may not be perfect for all scenarios
    # because in some cases, a transaction may somehow happen on a day for
    # which we don't have a closing price.  We should generally be okay,
    # though.
    trade_days = Decimal(trade_delta.days)
    xn_daily_perf = ((end_price - start_price) / start_price) / trade_days
    issuer_daily_perf = issuerdailyperf(sec_price_hist, repperson)
    if issuer_daily_perf is None:
        return irrelevant()

    if xn_daily_perf > issuer_daily_perf:
        relevant = 1
        success_or_failure = 1
    else:
        relevant = 1
        success_or_failure = 0

    if acq_or_disp == 'D' and success_or_failure == 1:
        success_or_failure = 0
    if acq_or_disp == 'D' and success_or_failure == 0:
        success_or_failure = 1

    return relevant, success_or_failure

# Remember to analyze the population of executives who are good traders
# against what population would be good traders by virtue of throwing
# darts.


def execanalyze(repperson, trade_delta):
    execentries =\
        Form345Entry.objects\
        .filter(reporting_owner_cik_num=repperson)\
        .filter(is_officer=True)\
        .exclude(transaction_date=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') |  # Open mkt / private purch
                Q(transaction_code='S') |  # Open mkt / private sale
                Q(transaction_code='I'))  # Discretionary 16b-3 Xn
    xns = 0
    buys = 0
    sells = 0
    good_xns = 0
    good_buys = 0
    good_sells = 0
    # Below can be changed freely to change whether the activity_threshold
    # is met.
    necessary_xns = 4
    necessary_buys = 1
    necessary_sales = 1

    entrydates =\
        list(Form345Entry.objects
             .filter(reporting_owner_cik_num=repperson)
             .exclude(is_officer=False)
             .order_by('filedatetime')
             .values_list('filedatetime', flat=True).distinct())
    exec_start = entrydates[0]
    exec_end = entrydates[-1]
    # Note that exec years is years as an SEC exec
    exec_years = Decimal((exec_end - exec_start).days) / Decimal(365.25)
    for execentry in execentries:
        xndate = execentry.transaction_date
        acq_or_disp = execentry.xn_acq_disp_code
        issuer = execentry.issuer_cik_num

        relevant, success_or_failure =\
            xnanalyze(repperson, xndate, acq_or_disp,
                      issuer, trade_delta)
        if relevant == 1:
            xns += 1

            if acq_or_disp == 'D':
                sells += 1
            else:
                buys += 1
        if relevant == 1 and success_or_failure == 1:
            good_xns += 1
            if acq_or_disp == 'D':
                good_sells += 1
            else:
                good_buys += 1
    tot_perf = Decimal(good_xns) / Decimal(xns)
    buy_perf = Decimal(good_buys) / Decimal(buys)
    sell_perf = Decimal(good_sells) / Decimal(sells)
    if xns >= necessary_xns and buys >= necessary_buys\
            and sells >= necessary_sales:
        activity_threshold = True
    else:
        activity_threshold = False

    ReportingPersonAtts(reporting_person=repperson,
                        transactions=xns,
                        buys=buys,
                        sells=sells,
                        activity_threshold=activity_threshold,
                        tot_perf=tot_perf,
                        buy_perf=buy_perf,
                        sell_perf=sell_perf,
                        exec_years=exec_years).save()

    return


def reviewreppersons(trade_delta):
    reppersonobjects =\
        Form345Entry.objects\
        .filter(is_officer=True)\
        .exclude(transaction_date=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') |  # Open mkt / private purch
                Q(transaction_code='S') |  # Open mkt / private sale
                Q(transaction_code='I'))  # Discretionary 16b-3 Xn
    reppersons =\
        reppersonobjects\
        .values_list('reporting_owner_cik', flat=True).distinct()
    for repperson in reppersons:
        execanalyze(repperson, trade_delta)
    return

reviewreppersons(trade_delta)
