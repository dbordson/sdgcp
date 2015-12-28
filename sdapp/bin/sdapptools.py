import datetime
from decimal import Decimal

from sdapp.models import ClosePrice


def median(medlist):
    if len(medlist) == 0:
        return Decimal(1)
    medlist.sort()
    i = len(medlist)/2
    if len(medlist) % 2 == 0:
        median_number = (medlist[i] + medlist[i-1])/2
    else:
        median_number = medlist[i]
    return median_number


def rep_none_with_zero(inputvar):
    if inputvar is not None:
        return inputvar
    else:
        return Decimal(0)


def is_none_or_zero(inputvar):
    if inputvar is None:
        return True
    elif inputvar == Decimal(0):
        return True
    else:
        return False


def laxer_start_price(sec_price_hist, pricedate):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__gte=pricedate-wkd_td)\
        .filter(close_date__lte=pricedate).order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_price(sph_obj, pricedate, price_dict):
    if sph_obj is None:
        return None, price_dict
    if type(sph_obj) is int:
        sph_pk = sph_obj
    else:
        sph_pk = sph_obj.pk
    if (sph_pk, pricedate) in price_dict:
        return price_dict[sph_pk, pricedate]
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sph_pk)\
        .filter(close_date=pricedate)
    if close_price.exists():
        price_dict[sph_pk, pricedate] = close_price[0].adj_close_price
        return close_price[0].adj_close_price
    else:
        laxer_price = laxer_start_price(sph_pk, pricedate)
        price_dict[sph_pk, pricedate] = laxer_price
        return laxer_price


def price_decline(sph_obj, date, timedelta, sp_dict):
    earlier_price =\
        get_price(sph_obj, date, sp_dict)
    later_price =\
        get_price(sph_obj, date + timedelta, sp_dict)
    if earlier_price > later_price:
        return True
    else:
        return False


def price_perf(sph_obj, date, timedelta, sp_dict):
    earlier_price =\
        get_price(sph_obj, date, sp_dict)
    later_price =\
        get_price(sph_obj, date + timedelta, sp_dict)
    if earlier_price is None or later_price is None\
            or earlier_price is Decimal(0):
        return None
    else:
        return (later_price / earlier_price) - Decimal(1)


def post_sale_perf(forms, sph_obj, timedelta, sp_dict):
    perf_l = []
    shares_l = []
    for form in forms:
        xn_price_perf =\
            price_perf(sph_obj, form.transaction_date, timedelta, sp_dict)
        xn_shares = form.transaction_shares
        adj_factor = form.adjustment_factor
        if xn_price_perf is not None\
                and xn_shares is not None:
            perf_l.append(xn_price_perf)
            shares_l.append(xn_shares * adj_factor)
    if len(perf_l) == 1:
        return perf_l[0]
    if len(perf_l) > 1:
        post_sale_perf =\
            sum(x * y for x, y in zip(perf_l, shares_l)) / sum(shares_l)
        return post_sale_perf
    else:
        return None
