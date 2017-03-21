import datetime
from decimal import Decimal
import gc
import sys

import django.db
from django.db.models import F, Q

from sdapp.bin.globals import (
    abs_sig_min, buyer, grant_period_calc_lookback, hist_sale_period,
    min_day_gap_for_10b51_trigger_sell_rate, now,
    price_trigger_lookback, seller, recent_sale_period, today, todaymid,
    tracking_period_calendar_years, trigger_min_stock_move)
from sdapp.bin.sdapptools import (
    get_price, get_sph_pk, median, is_none_or_zero, post_xn_perf,
    price_perf, rep_none_with_zero
)
from sdapp.models import (Affiliation, Form345Entry,
                          IssuerCIK, SecurityPriceHist)


def queryset_iterator(queryset, chunksize=50000):
    # Iterate over a Django Queryset ordered by the primary key

    # This method loads a maximum of chunksize (default: 1000) rows in it's
    # memory at the same time while django normally would load all rows in it's
    # memory. Using the iterator() method only causes it to not preload all the
    # classes.

    # Note that the implementation of the iterator does not support ordered
    # query sets.
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        django.db.reset_queries()
        gc.collect()


def fill_in_form_data():
    print 'Filling in primary equivalent and form value data...'
    print '    ...sorting...'
    xns = Form345Entry.objects\
        .filter(xn_full_conv_cost=None)\
        .exclude(security=None)\
        .exclude(xn_acq_disp_code=None)\
        .exclude(prim_security=None)
    if not xns.exists():
        print '    ....no new transactions; done.'
        return
    # xns = xns\
    #     .values(
    #         'conversion_price', 'deriv_or_nonderiv', 'pk', 'prim_security',
    #         'security', 'transaction_date', 'transaction_shares',
    #         'underlying_shares', 'underlying_security')
    counter = 0.0
    looplength = float(xns.count())
    price_dict = {}
    sph_pk_dict = {}
    print '    ...updating...'
    for x in queryset_iterator(xns):
        counter += 1.0
        # Do we price security directly or underlying?
        # Simplest case - what if the security is the primary security
        conversion_price = rep_none_with_zero(x.conversion_price)
        deriv_or_nonderiv = x.deriv_or_nonderiv
        prim_security = x.prim_security
        prim_security_sph_pk = get_sph_pk(prim_security, sph_pk_dict)
        security = x.security
        security_sph_pk = get_sph_pk(security, sph_pk_dict)
        if x.transaction_date is not None:
            xn_date = x.transaction_date
        else:
            xn_date = x.filedatetime.date
        xn_shares = x.transaction_shares
        xn_acq_disp_code = x.xn_acq_disp_code
        underlying_security = x.underlying_security
        underlying_security_sph_pk =\
            get_sph_pk(underlying_security, sph_pk_dict)
        underlying_shares = x.underlying_shares

        if xn_acq_disp_code == 'A':
            xn_sign = Decimal(1)
        elif xn_acq_disp_code == 'D':
            xn_sign = Decimal(-1)
        else:
            print '\nno transaction acq_or_disp code error for item pk', x.pk
            print 'acq_or_disp is neither "A" nor "D"\n'
            continue
        prim_price = get_price(prim_security_sph_pk, xn_date, price_dict)
        xn_value = None

        # Calc conversion costs
        if underlying_shares is not None:
            xn_full_conv_cost = underlying_shares * conversion_price
        elif xn_shares is not None:
            xn_full_conv_cost = xn_shares * conversion_price
        else:
            xn_full_conv_cost = Decimal(0)

        # Calc xn_value
        if security.pk == prim_security.pk:
            security_price = prim_price
            if prim_price is not None and xn_shares is not None:
                xn_value = xn_shares * prim_price * xn_sign
            else:
                xn_value = None
        # What if not primary security but is nonderivative
        elif deriv_or_nonderiv == 'N':
            if security_sph_pk is not None:
                security_price =\
                    get_price(security_sph_pk, xn_date, price_dict)
            else:
                security_price = None
            if security_price is not None and xn_shares is not None:
                xn_value = xn_shares * security_price * xn_sign
            else:
                xn_value = None
        # Now we deal with derivative securities
        # If there is direct pricing of the derivative (like class a
        # convertible into class b).
        elif deriv_or_nonderiv == 'D' and\
                security_sph_pk is not None:
            security_price = get_price(security_sph_pk, xn_date, price_dict)
            if security_price is not None and xn_shares is not None:
                xn_value = xn_shares * security_price * xn_sign
            else:
                xn_value = None
        # If no direct pricing of derivative, but have underlying pricing.
        elif deriv_or_nonderiv == 'D' and\
                security_sph_pk is None and\
                underlying_security_sph_pk is not None:
            underlying_price =\
                get_price(underlying_security_sph_pk, xn_date, price_dict)
            if underlying_price is not None and underlying_shares is not None:
                gross_value = underlying_shares * underlying_price
                xn_value = \
                    max(gross_value - xn_full_conv_cost, Decimal(0)) * xn_sign
            else:
                xn_value = None
        elif deriv_or_nonderiv != 'D' and deriv_or_nonderiv != 'N':
            print '\nError, deriv or nonderiv is blank for', x
            print '\n'
            continue
        else:
            continue

        # Calc primary share equivalents
        if security_sph_pk == prim_security_sph_pk and xn_shares is not None:
            xn_prim_share_eq = xn_shares * xn_sign
        elif underlying_security_sph_pk == prim_security_sph_pk\
                and underlying_shares is not None:
            xn_prim_share_eq = underlying_shares * xn_sign
        elif prim_price is not None and xn_value is not None:
            xn_prim_share_eq = xn_value / prim_price
        else:
            xn_prim_share_eq = None

        x.xn_prim_share_eq = xn_prim_share_eq
        x.xn_value = xn_value
        x.xn_full_conv_cost = xn_full_conv_cost
        x.save()

        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s forms to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n   done.'
    return


def price_reponse_count(
        sph_obj, enddate, td, sp_dict, perf_sign):
    period_price_perf =\
        price_perf(sph_obj, enddate, td, sp_dict)
    if period_price_perf is None:
        favorable_outcome = 0
        measured_outcome = 0
        return favorable_outcome, measured_outcome
    elif period_price_perf * perf_sign > Decimal(0):
        favorable_outcome = 1
        measured_outcome = 1
        return favorable_outcome, measured_outcome
    else:
        favorable_outcome = 0
        measured_outcome = 1
        return favorable_outcome, measured_outcome


def update_xn_counts(
        period_xns, acq_or_disp, sph_obj, enddate,
        sp_dict):
    td3mo = datetime.timedelta(91)
    td6mo = datetime.timedelta(182)
    td9mo = datetime.timedelta(275)
    td12mo = datetime.timedelta(365)
    if acq_or_disp == 'A':
        perf_sign = Decimal(1)
    else:
        perf_sign = Decimal(-1)

    if period_xns.exists():
        qtr_with_disc_xns_in_tracking_period = 1

        xn_qtr_3_mo_favorable, xn_qtr_3_mo_measured =\
            price_reponse_count(
                sph_obj, enddate, td3mo, sp_dict, perf_sign)

        xn_qtr_6_mo_favorable, xn_qtr_6_mo_measured =\
            price_reponse_count(
                sph_obj, enddate, td6mo, sp_dict, perf_sign)

        xn_qtr_9_mo_favorable, xn_qtr_9_mo_measured =\
            price_reponse_count(
                sph_obj, enddate, td9mo, sp_dict, perf_sign)

        xn_qtr_12_mo_favorable, xn_qtr_12_mo_measured =\
            price_reponse_count(
                sph_obj, enddate, td12mo, sp_dict, perf_sign)

        return qtr_with_disc_xns_in_tracking_period,\
            xn_qtr_3_mo_favorable, xn_qtr_3_mo_measured,\
            xn_qtr_6_mo_favorable, xn_qtr_6_mo_measured,\
            xn_qtr_9_mo_favorable, xn_qtr_9_mo_measured,\
            xn_qtr_12_mo_favorable, xn_qtr_12_mo_measured
    else:
        return 0,\
            0, 0, 0, 0,\
            0, 0, 0, 0


def calc_response_quarters(
        xn_forms, years, acq_or_disp, sph_obj, sp_dict):
    month_day_tuples =\
        [[1, 1, 3, 31],
         [4, 1, 6, 30],
         [7, 1, 9, 30],
         [10, 1, 12, 31]]
    qtrs_with_disc_xns_in_tracking_period = 0
    xn_qtrs_3_mo_favorable = 0
    xn_qtrs_6_mo_favorable = 0
    xn_qtrs_9_mo_favorable = 0
    xn_qtrs_12_mo_favorable = 0

    xn_qtrs_3_mo_measured = 0
    xn_qtrs_6_mo_measured = 0
    xn_qtrs_9_mo_measured = 0
    xn_qtrs_12_mo_measured = 0

    for year in years:
        for startmonth, startday, endmonth, endday in month_day_tuples:
            startdate = datetime.date(year, startmonth, startday)
            enddate = datetime.date(year, endmonth, endday)
            total_period_xns = xn_forms\
                .filter(transaction_date__gte=startdate)\
                .filter(transaction_date__lte=enddate)

            qtr_with_disc_xns_in_tracking_period,\
                xn_qtr_3_mo_favorable, xn_qtr_3_mo_measured,\
                xn_qtr_6_mo_favorable, xn_qtr_6_mo_measured,\
                xn_qtr_9_mo_favorable, xn_qtr_9_mo_measured,\
                xn_qtr_12_mo_favorable, xn_qtr_12_mo_measured =\
                update_xn_counts(
                    total_period_xns, acq_or_disp, sph_obj, enddate,
                    sp_dict)
            qtrs_with_disc_xns_in_tracking_period +=\
                qtr_with_disc_xns_in_tracking_period
            xn_qtrs_3_mo_favorable += xn_qtr_3_mo_favorable
            xn_qtrs_6_mo_favorable += xn_qtr_6_mo_favorable
            xn_qtrs_9_mo_favorable += xn_qtr_9_mo_favorable
            xn_qtrs_12_mo_favorable += xn_qtr_12_mo_favorable

            xn_qtrs_3_mo_measured += xn_qtr_3_mo_measured
            xn_qtrs_6_mo_measured += xn_qtr_6_mo_measured
            xn_qtrs_9_mo_measured += xn_qtr_9_mo_measured
            xn_qtrs_12_mo_measured += xn_qtr_12_mo_measured
    return qtrs_with_disc_xns_in_tracking_period,\
        xn_qtrs_3_mo_favorable, xn_qtrs_3_mo_measured,\
        xn_qtrs_6_mo_favorable, xn_qtrs_6_mo_measured,\
        xn_qtrs_9_mo_favorable, xn_qtrs_9_mo_measured,\
        xn_qtrs_12_mo_favorable, xn_qtrs_12_mo_measured


def sale_perf_attributes(issuer, reporting_owner):
    sp_dict = {}
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.exists():
        sph_obj = primary_tickers[0]
    else:
        return
    a = Affiliation.objects\
        .get(issuer=issuer, reporting_owner=reporting_owner)
    todayyear = today.year
    startyear = todayyear - tracking_period_calendar_years
    years = range(startyear, todayyear + 1)
    test_begin_date = datetime.date(startyear, 1, 1)
    td3mo = datetime.timedelta(91)
    td6mo = datetime.timedelta(182)
    td9mo = datetime.timedelta(275)
    td12mo = datetime.timedelta(365)

    xn_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(transaction_date__gte=F('filedatetime') +
                datetime.timedelta(-10))\
        .filter(transaction_date__gte=test_begin_date)\
        .filter(transaction_date__lt=today - recent_sale_period)\
        .exclude(xn_price_per_share=None)\
        .exclude(transaction_shares=None)
    # Sales
    sale_forms_disc = xn_forms.filter(transaction_code='S')\
        .exclude(tenbfive_note=True)
    acq_or_disp = 'D'
    a.qtrs_with_disc_sales_in_tracking_period,\
        a.sale_qtr_ct_3_mo_decline_disc, a.sale_qtr_ct_3_mo_measured_disc,\
        a.sale_qtr_ct_6_mo_decline_disc, a.sale_qtr_ct_6_mo_measured_disc,\
        a.sale_qtr_ct_9_mo_decline_disc, a.sale_qtr_ct_9_mo_measured_disc,\
        a.sale_qtr_ct_12_mo_decline_disc, a.sale_qtr_ct_12_mo_measured_disc =\
        calc_response_quarters(
            sale_forms_disc, years, acq_or_disp, sph_obj, sp_dict)
    a.post_sale_perf_3mo_disc =\
        post_xn_perf(sale_forms_disc, sph_obj, td3mo, sp_dict)
    a.post_sale_perf_6mo_disc =\
        post_xn_perf(sale_forms_disc, sph_obj, td6mo, sp_dict)
    a.post_sale_perf_9mo_disc =\
        post_xn_perf(sale_forms_disc, sph_obj, td9mo, sp_dict)
    a.post_sale_perf_12mo_disc =\
        post_xn_perf(sale_forms_disc, sph_obj, td12mo, sp_dict)

    # Buys
    buy_forms = xn_forms.filter(transaction_code='P')
    acq_or_disp = 'A'
    a.qtrs_with_buys_in_tracking_period,\
        a.buy_qtr_ct_3_mo_increase, a.buy_qtr_ct_3_mo_measured,\
        a.buy_qtr_ct_6_mo_increase, a.buy_qtr_ct_6_mo_measured,\
        a.buy_qtr_ct_9_mo_increase, a.buy_qtr_ct_9_mo_measured,\
        a.buy_qtr_ct_12_mo_increase, a.buy_qtr_ct_12_mo_measured =\
        calc_response_quarters(
            buy_forms, years, acq_or_disp, sph_obj, sp_dict)
    a.post_buy_perf_3mo =\
        post_xn_perf(buy_forms, sph_obj, td3mo, sp_dict)
    a.post_buy_perf_6mo =\
        post_xn_perf(buy_forms, sph_obj, td6mo, sp_dict)
    a.post_buy_perf_9mo =\
        post_xn_perf(buy_forms, sph_obj, td9mo, sp_dict)
    a.post_buy_perf_12mo =\
        post_xn_perf(buy_forms, sph_obj, td12mo, sp_dict)

    # 10b5_1
    sale_forms_10b = xn_forms.filter(transaction_code='S')\
        .filter(tenbfive_note=True)
    acq_or_disp = 'D'
    a.qtrs_with_10b_sales_in_tracking_period,\
        a.sale_qtr_ct_3_mo_decline_10b, a.sale_qtr_ct_3_mo_measured_10b,\
        a.sale_qtr_ct_6_mo_decline_10b, a.sale_qtr_ct_6_mo_measured_10b,\
        a.sale_qtr_ct_9_mo_decline_10b, a.sale_qtr_ct_9_mo_measured_10b,\
        a.sale_qtr_ct_12_mo_decline_10b, a.sale_qtr_ct_12_mo_measured_10b =\
        calc_response_quarters(
            sale_forms_10b, years, acq_or_disp, sph_obj, sp_dict)
    a.post_sale_perf_3mo_10b =\
        post_xn_perf(sale_forms_10b, sph_obj, td3mo, sp_dict)
    a.post_sale_perf_6mo_10b =\
        post_xn_perf(sale_forms_10b, sph_obj, td6mo, sp_dict)
    a.post_sale_perf_9mo_10b =\
        post_xn_perf(sale_forms_10b, sph_obj, td9mo, sp_dict)
    a.post_sale_perf_12mo_10b =\
        post_xn_perf(sale_forms_10b, sph_obj, td12mo, sp_dict)

    td_since_begin = today - test_begin_date
    cumulativeperformance =\
        price_perf(sph_obj, test_begin_date,
                   td_since_begin, sp_dict)
    years_since_begin = Decimal(td_since_begin.days) / Decimal(365)
    if cumulativeperformance is not None:
        a.annualized_perf_in_tracking_period =\
            (cumulativeperformance +
             Decimal(1))**(Decimal(1)/years_since_begin)\
            - Decimal(1)
    a.save()
    return


def calc_holdings(issuer, reporting_owner, sec_ids, prim_sec_id, calc_dt,
                  price_dict, ticker_sec_dict):
    calc_date = calc_dt.date()
    prim_price = get_price(ticker_sec_dict[prim_sec_id],
                           calc_date, price_dict)
    if prim_price is None or prim_price == Decimal(0):
        return None, None, None, None
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .exclude(filedatetime__gt=calc_dt)\
        .exclude(supersededdt__lte=calc_dt)\
        .exclude(shares_following_xn=None)\
        .values('shares_following_xn', 'adjustment_factor',
                'security__conversion_multiple', 'conversion_price',
                'security', 'underlying_security')
    total_shares_held = Decimal(0)
    total_value = Decimal(0)
    total_conv_cost = Decimal(0)
    for h in holdings:
        # Do we price security directly or underlying?
        if h['security'] in ticker_sec_dict:
            sec_id = h['security']
            underlying_conversion_mult = Decimal(1)
        else:
            sec_id = h['underlying_security']
            underlying_conversion_mult = h['security__conversion_multiple']
        # If pricing secondary security, calculate conversion multiple.
        if sec_id != prim_sec_id:
            holding_price = get_price(ticker_sec_dict[sec_id],
                                      calc_date, price_dict)
            if holding_price is None or prim_price is None or\
                    prim_price == Decimal(0):
                continue
            share_conversion_mult_to_primary_ticker = \
                holding_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)
        security_shares = h['shares_following_xn'] * h['adjustment_factor'] *\
            underlying_conversion_mult
        prim_eq_shares = security_shares *\
            share_conversion_mult_to_primary_ticker
        price = get_price(ticker_sec_dict[sec_id], calc_date, price_dict)
        if price is None or price == Decimal(0):
            continue
        adj_conversion_price = rep_none_with_zero(h['conversion_price']) /\
            h['adjustment_factor']
        holding_value = security_shares *\
            max(Decimal(0), price - adj_conversion_price)
        conv_cost = adj_conversion_price * security_shares
        total_shares_held += prim_eq_shares
        total_value += holding_value
        total_conv_cost += conv_cost
    if total_shares_held != Decimal(0):
        avg_conv_price = total_conv_cost / total_shares_held
        conv_to_price_ratio = avg_conv_price / prim_price
    else:
        avg_conv_price = None
        conv_to_price_ratio = None
    return total_shares_held, avg_conv_price, total_value, conv_to_price_ratio


def calc_equity_grants(issuer, reporting_owner, sec_ids, prim_sec_id,
                       price_dict, ticker_sec_dict):
    grants = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(transaction_code='A')\
        .exclude(transaction_shares=None)\
        .exclude(transaction_date=None)\
        .filter(transaction_date__gte=today - grant_period_calc_lookback -
                datetime.timedelta(5))\
        .filter(filedatetime__gte=todaymid - grant_period_calc_lookback)
    grant_dates = \
        list(grants.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no grant info available
    if len(grant_dates) == 0:
        return Decimal(0), Decimal(0), 1
    # If you have only one grant, assume annual because that is typical
    if len(grant_dates) == 1:
        grants_per_year = 1
    # Otherwise, figure out grants per year received based on spacing
    else:
        day_gaps = []
        for first_date, second_date in zip(grant_dates, grant_dates[1:]):
            day_gaps.append(Decimal((second_date - first_date).days))
        median_day_gap = median(day_gaps)
        day_gap_options = [Decimal(30), Decimal(45), Decimal(60),
                           Decimal(91), Decimal(182), Decimal(365)]
        estimated_day_gap = min(day_gap_options,
                                key=lambda x: abs(x-median_day_gap))
        grants_per_year = int(round(Decimal(365) / estimated_day_gap, 0))
    # now calc grant amounts in last year and use total to annualize
    grant_dates.reverse()
    last_year_dates = grant_dates[:grants_per_year]
    grants_amounts = grants\
        .filter(transaction_date__in=last_year_dates)\
        .values('xn_prim_share_eq', 'xn_full_conv_cost',
                'prim_adjustment_factor')
    # If no grants in last year, stop here.
    if grants_amounts.count() == 0:
        return Decimal(0), Decimal(0), 1
    # Otherwise calculate total grants
    annual_grant_shares = Decimal(0)
    total_conv_cost = Decimal(0)
    for g in grants_amounts:
        xn_prim_share_eq = g['xn_prim_share_eq']
        xn_full_conv_cost = g['xn_full_conv_cost']
        prim_adjustment_factor = g['prim_adjustment_factor']
        annual_grant_shares += rep_none_with_zero(xn_prim_share_eq)\
            * prim_adjustment_factor
        total_conv_cost += rep_none_with_zero(xn_full_conv_cost)
    #
    if annual_grant_shares != Decimal(0):
        avg_conv_price = total_conv_cost / annual_grant_shares
    else:
        avg_conv_price = None
    #
    return annual_grant_shares, avg_conv_price, grants_per_year


def calc_disc_xns(issuer, reporting_owner, sec_ids, prim_sec_id,
                  price_dict, ticker_sec_dict, startdate, enddate,
                  is_10b5_1):
    disc_xns = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)\
        .exclude(transaction_shares=None)
    if is_10b5_1 is True:
        disc_xns = disc_xns.filter(tenbfive_note=True)
    else:
        disc_xns = disc_xns.exclude(tenbfive_note=True)
    disc_xns = disc_xns\
        .values('xn_prim_share_eq', 'xn_value',
                'prim_adjustment_factor')
    if len(disc_xns) is 0:
        return Decimal(0), Decimal(0)
    net_xn_shares = Decimal(0)
    net_xn_value = Decimal(0)
    for x in disc_xns:
        xn_prim_share_eq = x['xn_prim_share_eq']
        xn_value = x['xn_value']
        prim_adjustment_factor = x['prim_adjustment_factor']

        net_xn_shares += rep_none_with_zero(xn_prim_share_eq)\
            * prim_adjustment_factor
        net_xn_value += rep_none_with_zero(xn_value)
    return net_xn_shares, net_xn_value


def hist_net_xn_clusters_per_year(
        issuer, reporting_owner, sec_ids,
        prim_sec_id, price_dict, ticker_sec_dict,
        startdate, enddate, is_10b5_1):
    sales = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(transaction_code='S')\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)\
        .exclude(transaction_shares=None)
    if is_10b5_1:
        sales = sales.filter(tenbfive_note=True)
    else:
        sales = sales.exclude(tenbfive_note=True)
    sale_dates = \
        list(sales.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no sale info available
    if len(sale_dates) == 0:
        sales_per_year = 0
    # If you have only one sale, assume annual because that is typical
    elif len(sale_dates) == 1:
        sales_per_year = 1
    # Otherwise, figure out sales per year received based on spacing
    else:
        day_gaps = []
        for first_date, second_date in zip(sale_dates, sale_dates[1:]):
            gap = Decimal((second_date - first_date).days)
            if gap > min_day_gap_for_10b51_trigger_sell_rate:
                day_gaps.append(gap)
        if len(day_gaps) == 0:
            return None
        median_day_gap = median(day_gaps)
        day_gap_options = [Decimal(14), Decimal(15), Decimal(30), Decimal(45),
                           Decimal(60), Decimal(91), Decimal(182),
                           Decimal(365)]
        estimated_day_gap = min(day_gap_options,
                                key=lambda x: abs(x-median_day_gap))
        sales_per_year = int(round(Decimal(365) / estimated_day_gap, 0))
    return sales_per_year


def recent_dates_prices(
        issuer, reporting_owner, sec_ids, prim_sec_id, price_dict,
        ticker_sec_dict, startdate, enddate, is_10b5_1):
    sales = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .filter(Q(transaction_code='S') |
                Q(transaction_code='P'))\
        .exclude(transaction_shares=None)\
        .filter(transaction_date__gte=startdate)\
        .filter(transaction_date__lte=enddate)
    if is_10b5_1:
        sales = sales.filter(tenbfive_note=True)
    else:
        sales = sales.exclude(tenbfive_note=True)
    sale_dates = \
        list(sales.order_by('transaction_date')
             .values_list('transaction_date', flat=True).distinct())
    # Do not pass go if no 10b5-1 info available
    if len(sale_dates) == 0:
        transaction_date_price_info = []
    else:
        transaction_date_price_info = []
        for date in sale_dates:
            price = get_price(ticker_sec_dict[prim_sec_id],
                              date, price_dict)
            transaction_date_price_info.append((date, price))

    return transaction_date_price_info


def calc_increase_in_xns(
        abs_sig_min, acq_or_disp, aff, expected_recent_xn_amount,
        is_10b5_1, issuer, price_dict, prim_sec_id, recent,
        recent_val, reporting_owner, ticker_sec_dict, ticker_sec_ids,
        transaction_date_price_info):
    if acq_or_disp == 'D':
        xn_sign = Decimal(-1)
    elif acq_or_disp == 'A':
        xn_sign = Decimal(1)
    else:
        print 'error acq_or_disp is invalid value'
        raise ValueError
    # Determine if expected sale rate exceeded.
    # Remember considerations regarding sign -- sales are negative.
    if expected_recent_xn_amount is not None and\
            recent * xn_sign > Decimal(0) and\
            len(transaction_date_price_info) != 0 and\
            recent * xn_sign > expected_recent_xn_amount * xn_sign and\
            recent_val * xn_sign > abs_sig_min:
        increase_in_xns = True
        xn_days = len(transaction_date_price_info)
        total_net_xn_shares = Decimal(0)
        total_net_xn_value = Decimal(0)
        for date, price in transaction_date_price_info:
            startdate = date
            enddate = date
            net_xn_shares, net_xn_value =\
                calc_disc_xns(
                    issuer, reporting_owner, ticker_sec_ids,
                    prim_sec_id, price_dict, ticker_sec_dict,
                    startdate, enddate, is_10b5_1
                )
            total_net_xn_shares += net_xn_shares
            total_net_xn_value += net_xn_value
            # We tie the signal performance to the first transaction
            # to exceed the expected period sales.  This serves purposes
            # of consistency with any backtesting criteria and is more
            # logically defensible than first or last xns in period.
            if total_net_xn_shares * xn_sign >\
                    expected_recent_xn_amount * xn_sign and\
                    total_net_xn_value * xn_sign > abs_sig_min:
                xns_date = date
                xns_price = price
                xns_prior_performance =\
                    price_perf(
                        ticker_sec_dict[prim_sec_id],
                        date - price_trigger_lookback, price_trigger_lookback,
                        price_dict
                    )
                # if hist_lookback is True:
                #     subs_perf_date = date + perf_period_days_td
                # else:
                subs_perf_date = today
                xns_subs_performance =\
                    price_perf(
                        ticker_sec_dict[prim_sec_id],
                        date, subs_perf_date - date,
                        price_dict
                    )
                if xns_prior_performance * Decimal(-1) * xn_sign >\
                        trigger_min_stock_move:
                    price_trigger_detected = True
                else:
                    price_trigger_detected = False
                break
            else:
                price_trigger_detected = False
                xns_date = None
                xns_price = None
                xns_prior_performance = None
                xns_subs_performance = None
    #
    else:
        increase_in_xns = False
        price_trigger_detected = False
        xns_date = None
        xns_price = None
        xns_prior_performance = None
        xns_subs_performance = None
        xn_days = None
    return increase_in_xns, price_trigger_detected, xns_date, xns_price,\
        xns_prior_performance, xns_subs_performance, xn_days


def calc_person_affiliation(
        issuer, reporting_owner, price_dict):
    affiliation_forms = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)
    latest_form = affiliation_forms.latest('filedatetime')
    aff =\
        Affiliation.objects.get(issuer=issuer,
                                reporting_owner=reporting_owner)
    # General info
    aff.issuer_name = IssuerCIK.objects.get(cik_num=issuer).name
    aff.person_name = latest_form.reporting_owner_name
    aff.is_director = latest_form.is_director
    aff.is_officer = latest_form.is_officer
    aff.is_ten_percent = latest_form.is_ten_percent
    aff.is_something_else = latest_form.is_something_else
    aff.reporting_owner_title = latest_form.reporting_owner_title
    aff.latest_form_dt = latest_form.filedatetime
    first_form = affiliation_forms.earliest('filedatetime')
    aff.first_form_dt = first_form.filedatetime
    aff.is_active = True
    ticker_list = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None).values_list('security', 'pk')
    ticker_sec_dict = dict(ticker_list)
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True).exclude(security=None)
    # If no primary ticker, the numerical analysis is meaningless
    # This will catch errors if the script is run before db populated
    # of if a company's ticker wasn't linked. Should otherwise not happen.
    if primary_tickers.count() == 0:
        aff.save()
        return
    prim_ticker = primary_tickers[0]
    prim_sec_id = prim_ticker.security.pk
    all_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None)
    ticker_sec_ids = all_tickers.values_list('security', flat=True)

    # Populate current and prior shares, conv price, value, conv price ratio
    aff.share_equivalents_held, aff.average_conversion_price,\
        aff.share_equivalents_value, aff.conversion_to_price_ratio =\
        calc_holdings(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, todaymid, price_dict, ticker_sec_dict)

    prior_datetime = todaymid - recent_sale_period
    aff.prior_share_equivalents_held, aff.prior_average_conversion_price,\
        aff.prior_share_equivalents_value,\
        aff.prior_conversion_to_price_ratio =\
        calc_holdings(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, prior_datetime, price_dict,
                      ticker_sec_dict)

    # Populate grant rate info
    equity_grant_rate, aff.avg_grant_conv_price, grants_per_year =\
        calc_equity_grants(issuer, reporting_owner, ticker_sec_ids,
                           prim_sec_id, price_dict, ticker_sec_dict)
    aff.equity_grant_rate = equity_grant_rate
    # Recent / hist sale data
    recent_period_start = today - recent_sale_period
    hist_period_start = today - hist_sale_period

    # non-10b5-1
    is_10b5_1 = False
    recent_xns_shares_disc, recent_xns_value_disc =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, price_dict, ticker_sec_dict,
                      recent_period_start,
                      today, is_10b5_1)
    aff.recent_xns_shares_disc, aff.recent_xns_value_disc =\
        recent_xns_shares_disc, recent_xns_value_disc

    hist_xns_shares_disc, hist_xns_value_disc =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, price_dict, ticker_sec_dict,
                      hist_period_start,
                      recent_period_start, is_10b5_1)
    aff.hist_xns_shares_disc, aff.hist_xns_value_disc =\
        hist_xns_shares_disc, hist_xns_value_disc

    # Detect non-10b5-1 sale increases
    transaction_date_price_info = \
        recent_dates_prices(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
            price_dict, ticker_sec_dict, recent_period_start, today, is_10b5_1)
    # First determine if there is enough data to know expected selling rate.

    if not is_none_or_zero(recent_xns_shares_disc):
        if equity_grant_rate is None:
            equity_grant_rate = Decimal(0)
        recent = recent_xns_shares_disc
        recent_val = recent_xns_value_disc
        one_year_over_len_recent =\
            Decimal(365) /\
            Decimal((today - recent_period_start).days)

        expected_recent_share_sale_amount_disc =\
            min(Decimal(-1) * equity_grant_rate / one_year_over_len_recent,
                Decimal(-1) * equity_grant_rate / grants_per_year)
    else:
        recent = Decimal(0)
        recent_val = Decimal(0)
        one_year_over_len_recent = None
        expected_recent_share_sale_amount_disc = Decimal(0)

    increase_in_xns, price_selling, selling_date, selling_price,\
        selling_prior_performance, selling_subs_performance, xn_days =\
        calc_increase_in_xns(
            abs_sig_min, 'D', aff, expected_recent_share_sale_amount_disc,
            is_10b5_1, issuer, price_dict, prim_sec_id, recent,
            recent_val, reporting_owner, ticker_sec_dict, ticker_sec_ids,
            transaction_date_price_info)
    aff.increase_in_selling_disc = increase_in_xns
    aff.expected_recent_share_sale_amount_disc =\
        expected_recent_share_sale_amount_disc
    aff.selling_date_disc = selling_date
    aff.selling_close_price_disc = selling_price
    aff.selling_prior_performance_disc = selling_prior_performance
    aff.selling_subs_performance_disc = selling_subs_performance
    aff.price_motivated_sale_detected_disc = price_selling
    aff.xn_days_disc = xn_days

    # Detect non 10b5-1 buying
    expected_recent_share_buying_amount_disc = Decimal(0)
    increase_in_xns, price_buying, buying_date, buying_price,\
        buying_prior_performance, buying_subs_performance, xn_days =\
        calc_increase_in_xns(
            abs_sig_min, 'A', aff, expected_recent_share_buying_amount_disc,
            is_10b5_1, issuer, price_dict, prim_sec_id, recent,
            recent_val, reporting_owner, ticker_sec_dict, ticker_sec_ids,
            transaction_date_price_info)
    aff.increase_in_buying_disc = increase_in_xns
    aff.buying_date_disc = buying_date
    aff.buying_close_price_disc = buying_price
    aff.buying_prior_performance_disc = buying_prior_performance
    aff.buying_subs_performance_disc = buying_subs_performance
    aff.price_motivated_buy_detected_disc = price_buying

    # 10b5-1
    is_10b5_1 = True
    recent_xns_shares_10b5_1, recent_xns_value_10b5_1 =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, price_dict, ticker_sec_dict,
                      recent_period_start,
                      today, is_10b5_1)
    aff.recent_xns_shares_10b5_1, aff.recent_xns_value_10b5_1 =\
        recent_xns_shares_10b5_1, recent_xns_value_10b5_1

    hist_xns_shares_10b5_1, hist_xns_value_10b5_1 =\
        calc_disc_xns(issuer, reporting_owner, ticker_sec_ids,
                      prim_sec_id, price_dict, ticker_sec_dict,
                      hist_period_start,
                      recent_period_start, is_10b5_1)
    aff.hist_xns_shares_10b5_1, aff.hist_xns_value_10b5_1 =\
        hist_xns_shares_10b5_1, hist_xns_value_10b5_1
    # Detect 10b5-1 sale increases

    clusters_in_hist_period_10b5_1 =\
        hist_net_xn_clusters_per_year(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
            price_dict, ticker_sec_dict, hist_period_start,
            recent_period_start, is_10b5_1)
    transaction_date_price_info = \
        recent_dates_prices(
            issuer, reporting_owner, ticker_sec_ids, prim_sec_id,
            price_dict, ticker_sec_dict, recent_period_start, today, is_10b5_1)
    # First determine if there is enough data to know expected selling rate.
    # Note that if historical selling rate is zero, we do not proceed.  The
    # idea is that if no historical 10b5_1 selling, we don't count an increase
    #  -- in this case an increase in overall selling is relevant but not entry
    # into a 10b5_1 plan.  (Otherwise captures innocuous new plans)
    if not is_none_or_zero(recent_xns_shares_10b5_1) and\
            not is_none_or_zero(clusters_in_hist_period_10b5_1) and\
            hist_xns_shares_10b5_1 < Decimal(0) and\
            not is_none_or_zero(hist_xns_shares_10b5_1):
        recent = recent_xns_shares_10b5_1
        recent_val = recent_xns_value_10b5_1
        hist = hist_xns_shares_10b5_1
        len_hist_over_len_recent =\
            Decimal((recent_period_start - hist_period_start).days) /\
            Decimal((today - recent_period_start).days)
        expected_recent_share_sale_amount_10b5_1 =\
            min(hist / len_hist_over_len_recent,
                hist / clusters_in_hist_period_10b5_1)
    else:
        recent = Decimal(0)
        recent_val = Decimal(0)
        len_hist_over_len_recent = None
        expected_recent_share_sale_amount_10b5_1 = Decimal(0)

    increase_in_xns, price_trigger_detected, selling_date, selling_price,\
        selling_prior_performance, selling_subs_performance, xn_days =\
        calc_increase_in_xns(
            abs_sig_min, 'D', aff, expected_recent_share_sale_amount_10b5_1,
            is_10b5_1, issuer, price_dict, prim_sec_id, recent,
            recent_val, reporting_owner, ticker_sec_dict, ticker_sec_ids,
            transaction_date_price_info)
    aff.increase_in_selling_10b5_1 = increase_in_xns
    aff.expected_recent_share_sale_amount_10b5_1 =\
        expected_recent_share_sale_amount_10b5_1
    aff.selling_date_10b5_1 = selling_date
    aff.selling_close_price_10b5_1 = selling_price
    aff.selling_prior_performance_10b5_1 = selling_prior_performance
    aff.selling_subs_performance_10b5_1 = selling_subs_performance
    aff.price_trigger_detected_10b5_1 = price_trigger_detected
    aff.xn_days_10b5_1 = xn_days
    # Placeholder behavior calculation
    total_xn_shares = recent_xns_shares_disc + recent_xns_shares_10b5_1
    if total_xn_shares > Decimal(0):
        behavior = buyer
    elif aff.equity_grant_rate is not None\
            and Decimal(-1) * total_xn_shares\
            > aff.equity_grant_rate:
        behavior = seller
    elif aff.equity_grant_rate is None\
            and Decimal(-1) * total_xn_shares\
            > Decimal(0):
        behavior = seller
    else:
        behavior = None
    aff.behavior = behavior

    if aff.prior_share_equivalents_held >= 1000000000000\
            or aff.share_equivalents_held >= 1000000000000:
        print issuer, reporting_owner, aff.person_name
        print 'prior_share_equivalents_held',
        print aff.prior_share_equivalents_held
        print 'share_equivalents_held',
        print aff.share_equivalents_held
        print 'a number is too big'
        aff.prior_share_equivalents_held = 0
        aff.share_equivalents_held = 0

    aff.save()
    return


def upd():
    print 'Updating affiliations for new forms'
    print '...sorting...'
    affiliations_with_new_forms = Affiliation.objects.all()\
        .values_list('issuer', 'reporting_owner')
    counter = 0.0
    looplength = float(len(affiliations_with_new_forms))
    price_dict = {}
    print '...updating and saving...'
    for issuer, reporting_owner in affiliations_with_new_forms:
        calc_person_affiliation(
            issuer, reporting_owner, price_dict
        )
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliations to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()

    print '\n   ...determining who is active...'
    general_include_date = now - datetime.timedelta(3 * 365)
    no_shares_include_date = now - datetime.timedelta(365)
    officer_include_date = now - datetime.timedelta(400)
    # If officer and not 10%, use officer date.
    Affiliation.objects.filter(is_active=True)\
        .filter(is_officer=True).exclude(is_ten_percent=True)\
        .filter(latest_form_dt__lte=officer_include_date)\
        .update(is_active=False)
    # If officer and 10%, use gen include date (big owners may not
    # get annual stock grants, so give more time between transactions)
    Affiliation.objects.filter(is_active=True)\
        .filter(is_officer=True).filter(is_ten_percent=True)\
        .filter(latest_form_dt__lte=general_include_date)\
        .update(is_active=False)
    # If not an officer and have shares, just get general date
    Affiliation.objects.filter(is_active=True)\
        .filter(~Q(is_officer=True))\
        .filter(share_equivalents_held__gt=Decimal(0))\
        .filter(latest_form_dt__lte=general_include_date)\
        .update(is_active=False)
    # If not an officer and have no shares, get less time
    Affiliation.objects.filter(is_active=True)\
        .filter(~Q(is_officer=True))\
        .exclude(share_equivalents_held__gt=Decimal(0))\
        .filter(latest_form_dt__lte=no_shares_include_date)\
        .update(is_active=False)
    print '   ...active status updated.'
    return


def annotatestats():
    affiliations = Affiliation.objects.all()\
        .values_list(
            'issuer', 'reporting_owner', 'increase_in_selling_disc',
            'increase_in_buying_disc', 'increase_in_selling_10b5_1')
    affiliations.update(
        qtrs_with_disc_sales_in_tracking_period=None,
        sale_qtr_ct_3_mo_decline_disc=None,
        sale_qtr_ct_3_mo_measured_disc=None,
        sale_qtr_ct_6_mo_decline_disc=None,
        sale_qtr_ct_6_mo_measured_disc=None,
        sale_qtr_ct_9_mo_decline_disc=None,
        sale_qtr_ct_9_mo_measured_disc=None,
        sale_qtr_ct_12_mo_decline_disc=None,
        sale_qtr_ct_12_mo_measured_disc=None,
        post_sale_perf_3mo_disc=None,
        post_sale_perf_6mo_disc=None,
        post_sale_perf_9mo_disc=None,
        post_sale_perf_12mo_disc=None,
        qtrs_with_buys_in_tracking_period=None,
        buy_qtr_ct_3_mo_increase=None,
        buy_qtr_ct_3_mo_measured=None,
        buy_qtr_ct_6_mo_increase=None,
        buy_qtr_ct_6_mo_measured=None,
        buy_qtr_ct_9_mo_increase=None,
        buy_qtr_ct_9_mo_measured=None,
        buy_qtr_ct_12_mo_increase=None,
        buy_qtr_ct_12_mo_measured=None,
        post_buy_perf_3mo=None,
        post_buy_perf_6mo=None,
        post_buy_perf_9mo=None,
        post_buy_perf_12mo=None,
        qtrs_with_10b_sales_in_tracking_period=None,
        sale_qtr_ct_3_mo_decline_10b=None,
        sale_qtr_ct_3_mo_measured_10b=None,
        sale_qtr_ct_6_mo_decline_10b=None,
        sale_qtr_ct_6_mo_measured_10b=None,
        sale_qtr_ct_9_mo_decline_10b=None,
        sale_qtr_ct_9_mo_measured_10b=None,
        sale_qtr_ct_12_mo_decline_10b=None,
        sale_qtr_ct_12_mo_measured_10b=None,
        post_sale_perf_3mo_10b=None,
        post_sale_perf_6mo_10b=None,
        post_sale_perf_9mo_10b=None,
        post_sale_perf_12mo_10b=None,
        annualized_perf_in_tracking_period=None,
    )
    counter = 0.0
    looplength = float(len(affiliations))
    for issuer, reporting_owner, increase_in_selling_disc,\
            increase_in_buying_disc, increase_in_selling_10b5_1\
            in affiliations:
        top_holders = Affiliation.objects.filter(issuer=issuer)\
            .order_by('-share_equivalents_value')\
            .values_list('reporting_owner', flat=True)
        top_3_holders = list(top_holders)[:3]
        if reporting_owner in top_3_holders:
                # or increase_in_selling_disc or\
                # increase_in_buying_disc or increase_in_selling_10b5_1:
            sale_perf_attributes(issuer, reporting_owner)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliations to annotate: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
        django.db.reset_queries()
    print "\ndone."
    return


fill_in_form_data()
upd()
annotatestats()
