from decimal import Decimal
import sys

import django.db
from django.db.models import Q

from sdapp.bin.globals import (
    abs_sig_min, hist_sale_period, perf_period_days_td, price_trigger_lookback,
    recent_sale_period, today
)
from sdapp.models import (
    Affiliation, Form345Entry, SecurityPriceHist
)

from sdapp.bin.sdapptools import (
    get_price, price_perf, rep_none_with_zero
)

from sdapp.bin.update_affiliation_data import(
    calc_disc_xns, calc_increase_in_xns, calc_equity_grants,
    hist_net_xn_clusters_per_year, recent_dates_prices
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
        hist_period_start, is_10b5_1, acq_or_disp):
    hist_lookback = True

    recent_xn_shares, recent_xn_value =\
        calc_disc_xns(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, recent_period_start, transaction_date, is_10b5_1
        )

    if acq_or_disp == 'D':
        hist_xns_shares, hist_xns_value_disc =\
            calc_disc_xns(
                issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
                price_dict, ticker_sec_dict, hist_period_start,
                recent_period_start, is_10b5_1
            )
    else:
        hist_xns_shares =\
            None

    if acq_or_disp == 'D' and is_10b5_1 is True:
        clusters_in_hist_period =\
            hist_net_xn_clusters_per_year(
                issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
                price_dict, ticker_sec_dict, hist_period_start,
                recent_period_start, is_10b5_1
            )
        equity_grant_rate, avg_grant_conv_price, grants_per_year =\
            None, None, None

        cluster_rate = hist_xns_shares
        clusters_in_hist_period = clusters_in_hist_period

    else:
        clusters_in_hist_period = None
        equity_grant_rate, avg_grant_conv_price, grants_per_year =\
            calc_equity_grants(
                issuer, reporting_owner, ticker_sec_ids,
                prim_sec_id, price_dict, ticker_sec_dict
            )
        cluster_rate = Decimal(-1) * equity_grant_rate
        clusters_in_hist_period = grants_per_year

    transaction_date_price_info = \
        recent_dates_prices(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id, price_dict,
            ticker_sec_dict, recent_period_start, transaction_date, is_10b5_1
        )

    recent = recent_xn_shares

    len_hist_over_len_recent =\
        (hist_sale_period - recent_sale_period).days /\
        (recent_sale_period).days
    if acq_or_disp == 'A':
        exp_recent_rate = Decimal(0)
    elif rep_none_with_zero(cluster_rate) == 0 or\
            rep_none_with_zero(clusters_in_hist_period) == 0:
        exp_recent_rate = Decimal(0)
    else:
        exp_recent_rate = min(cluster_rate / len_hist_over_len_recent,
                              cluster_rate / clusters_in_hist_period)
    # Note that the signs are flipped below because we are looking
    # for the most negative quantities.
    increase_in_xns, price_selling, selling_date, selling_price,\
        selling_prior_performance, selling_subs_performance, xn_days =\
        calc_increase_in_xns(
            abs_sig_min, acq_or_disp, aff, exp_recent_rate, hist_lookback,
            is_10b5_1, issuer, price_dict, prim_sec_id, recent,
            recent_xn_value, reporting_owner, ticker_sec_dict, ticker_sec_ids,
            transaction_date_price_info)

    return increase_in_xns, recent_xn_value, selling_date,\
        selling_subs_performance


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
