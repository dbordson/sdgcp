from decimal import Decimal
import sys

import django.db
from django.db.models import Q

from sdapp.bin.globals import (
    hist_sale_period, perf_period_days_td, price_trigger_lookback,
    recent_sale_period, today
)
from sdapp.models import (
    Affiliation, Form345Entry, SecurityPriceHist
)

from sdapp.bin.sdapptools import (
    get_price, price_perf, rep_none_with_zero
)

from sdapp.bin.update_affiliation_data import(
    calc_disc_xns, hist_10b5_1_sales_per_year, recent_10b5_1_dates_prices
)


def weighted_avg(vector_input_weight_table):
    # input is tuple table formatted as
    # [[output1, weight1], [output2, weight2]...]
    if len(vector_input_weight_table) == 0:
        return None
    if len(vector_input_weight_table) == 1:
        return vector_input_weight_table[0][0]
    dotproduct = sum(p * q for p, q in vector_input_weight_table)
    divisor = sum(q for p, q in vector_input_weight_table)
    wavg = dotproduct / divisor
    return wavg


def calc_prior_trigger_perf_for_sale(
        aff, sale, issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
        price_dict, ticker_sec_dict, transaction_date, recent_period_start,
        hist_period_start, only_10b5_1
):

    recent_share_sell_rate_for_10b5_1_plans, recent_10b5_1_xn_value =\
        calc_disc_xns(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, recent_period_start, transaction_date, True
        )

    historical_share_sell_rate_for_10b5_1_plans, hist_10b5_1_xn_value =\
        calc_disc_xns(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, hist_period_start, recent_period_start, True
        )

    clusters_in_hist_period =\
        hist_10b5_1_sales_per_year(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, hist_period_start, recent_period_start
        )
    transaction_date_price_info = \
        recent_10b5_1_dates_prices(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, recent_period_start, transaction_date
        )
    recent = recent_share_sell_rate_for_10b5_1_plans
    hist = historical_share_sell_rate_for_10b5_1_plans
    len_hist_over_len_recent =\
        (hist_sale_period - recent_sale_period).days /\
        (recent_sale_period).days
    if rep_none_with_zero(hist) == 0 or\
            rep_none_with_zero(clusters_in_hist_period) == 0:
        exp_recent_rate = 0
    else:
        exp_recent_rate = min(hist / len_hist_over_len_recent,
                              hist / clusters_in_hist_period)
    # Note that the signs are flipped below because we are looking
    # for the most negative quantities.
    if recent < Decimal(0) and\
            hist < Decimal(0) and\
            clusters_in_hist_period is not None and\
            clusters_in_hist_period != 0 and\
            recent < exp_recent_rate and\
            len(transaction_date_price_info) != 0:

        trigger_10b5_1_price_perf =\
            price_perf(
                ticker_sec_dict[prim_sec_id],
                transaction_date - price_trigger_lookback,
                price_trigger_lookback, price_dict
            )

        if sale.security.pk in ticker_sec_dict:
            sec_id = sale.security.pk
            underlying_conversion_mult = Decimal(1)
        else:
            sec_id = sale.underlying_security.pk
            underlying_conversion_mult =\
                sale.security__conversion_multiple

        if sec_id != prim_sec_id and\
                sale.underlying_security.pk != prim_sec_id:
            sec_price = get_price(ticker_sec_dict[sec_id],
                                  transaction_date, price_dict)
            prim_price = get_price(ticker_sec_dict[prim_sec_id],
                                   transaction_date, price_dict)
            if sec_price is None or prim_price is None or\
                    prim_price == Decimal(0):
                return None, Decimal(0), Decimal(0)
            share_conversion_mult_to_primary_ticker = \
                sec_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)

        xn_sign = {'S': Decimal(-1), 'P': Decimal(1)}
        prim_eq_shares = sale.transaction_shares *\
            sale.adjustment_factor * underlying_conversion_mult *\
            xn_sign[sale.transaction_code] *\
            share_conversion_mult_to_primary_ticker
        if trigger_10b5_1_price_perf > Decimal(0):
            selling_subs_performance =\
                price_perf(
                    ticker_sec_dict[prim_sec_id], transaction_date,
                    perf_period_days_td, price_dict
                )
            return True, rep_none_with_zero(selling_subs_performance),\
                prim_eq_shares
        else:
            selling_subs_performance =\
                price_perf(
                    ticker_sec_dict[prim_sec_id], transaction_date,
                    perf_period_days_td, price_dict
                )
            return False, rep_none_with_zero(selling_subs_performance),\
                prim_eq_shares
    return None, Decimal(0), Decimal(0)


def calc_avg_avg_prior_trigger_performance(aff):
    price_dict = {}
    issuer = aff.issuer
    reporting_owner = aff.reporting_owner
    all_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None)
    ticker_sec_ids = all_tickers.values_list('security', flat=True)
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.count() == 0:
        return
    prim_ticker = primary_tickers[0]
    prim_sec_id = prim_ticker.security.pk

    ticker_list = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None).values_list('security', 'pk')
    ticker_sec_dict = dict(ticker_list)
    # Start date calculated to give enough history based on the assumption
    # that at detection, you should to look back the rest of the recent period
    # plus to the beginning of the historical period to find a anomalous 10b5-1
    # transaction.
    start_date =\
        aff.first_form_dt.date() + hist_sale_period + recent_sale_period
    aff_recent_period_start = today - recent_sale_period
    sales = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=ticker_sec_ids) |
                Q(underlying_security__in=ticker_sec_ids))\
        .filter(transaction_code='S')\
        .exclude(transaction_shares=None)\
        .filter(transaction_date__gte=start_date)\
        .filter(transaction_date__lte=aff_recent_period_start)\
        .filter(tenbfive_note=True)
    all_10b5_1_sales = []
    trigger_sales_10b5_1 = []
    for sale in sales:
        transaction_date = sale.transaction_date
        recent_period_start = transaction_date - recent_sale_period
        hist_period_start = transaction_date - hist_sale_period

        is_trigger, subs_perf, shares = \
            calc_prior_trigger_perf_for_sale(
                aff, sale, issuer, reporting_owner, ticker_sec_ids,
                prim_sec_id, price_dict, ticker_sec_dict, transaction_date,
                recent_period_start, hist_period_start, True
            )
        # Note that is_trigger can equal None
        if is_trigger is True:
            trigger_sales_10b5_1.append([subs_perf, shares])
            all_10b5_1_sales.append([subs_perf, shares])
        if is_trigger is False:
            all_10b5_1_sales.append([subs_perf, shares])

    aff.avg_prior_trigger_perf = weighted_avg(all_10b5_1_sales)
    aff.num_in_avg_prior_trigger_perf = len(all_10b5_1_sales)
    aff.avg_prior_10b5_1_trigger_perf = weighted_avg(trigger_sales_10b5_1)
    aff.num_in_avg_prior_10b5_1_trigger_perf = len(trigger_sales_10b5_1)
    aff.save()


affs_for_update = Affiliation.objects.filter(increase_in_10b5_1_selling=True)
counter = 0.0
looplength = float(len(affs_for_update))
for aff in affs_for_update:
    calc_avg_avg_prior_trigger_performance(aff)
    counter += 1.0
    percentcomplete = round(counter / looplength * 100, 2)
    sys.stdout.write("\r%s / %s affiliations avg perf to update: %.2f%%" %
                     (int(counter), int(looplength), percentcomplete))
    sys.stdout.flush()
    django.db.reset_queries()
