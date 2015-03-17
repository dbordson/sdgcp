from sdapp.models import SecurityPriceHist, ClosePrice, Form345Entry
import datetime
from decimal import Decimal

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
             .values_list('filedatetime'))
    first_date = entry_dates[0].date()
    last_date = entry_dates[-1].date()
    days = Decimal(((last_date - first_date).days))
    if days < 365:
        return None
    first_price = get_price(sec_price_hist, first_date)
    last_price = get_price(sec_price_hist, last_date)
    if first_price is None or last_price is None:
        return None
    daily_return = ((last_price - first_price) / first_price) / days

    return daily_return


def xnanalyze(repperson, xndate, acq_or_disp, issuer, trade_delta):
    sec_price_hist_qs = SecurityPriceHist.objects.filter(issuer)
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
