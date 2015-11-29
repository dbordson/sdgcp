import datetime
from decimal import Decimal
import sys

import django.db
from django.db.models import F, Q

from sdapp.bin.globals import (buyer, now, today, todaymid, seller,
                               signal_detect_lookback)
from sdapp.models import (Affiliation, ClosePrice, Form345Entry,
                          IssuerCIK, SecurityPriceHist)


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


def calc_disc_xn_shares(issuer, reporting_owner, security):
    other_ticker_securities = SecurityPriceHist.objects\
        .filter(issuer=issuer).exclude(security=security)\
        .exclude(security=None)\
        .values_list('security', flat=True)
    a = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .exclude(security__in=other_ticker_securities)\
        .filter(Q(security=security) | Q(underlying_security=security))\
        .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
        .filter(transaction_date__gte=F('filedatetime') +
                datetime.timedelta(-10))\
        .filter(transaction_date__gte=today + signal_detect_lookback)\
        .exclude(transaction_shares=None)\
        .exclude(xn_acq_disp_code=None)
    net_xn_shares = Decimal(0)
    for item in a:
        if item.xn_acq_disp_code == 'D':
            sign_transaction_shares = \
                Decimal(-1) * item.transaction_shares * item.adjustment_factor\
                * item.security.conversion_multiple
        else:
            sign_transaction_shares = \
                item.transaction_shares * item.adjustment_factor\
                * item.security.conversion_multiple
        net_xn_shares += sign_transaction_shares

    return net_xn_shares


def calc_grants(issuer_cik, reporting_person_cik, security):
    grants = Form345Entry.objects.filter(issuer_cik=issuer_cik)\
        .filter(reporting_owner_cik=reporting_person_cik)\
        .filter(Q(security=security) | Q(underlying_security=security))\
        .filter(transaction_code='A')\
        .filter(transaction_date__gte=today - datetime.timedelta(735))\
        .filter(filedatetime__gte=todaymid - datetime.timedelta(730))
    grant_dates = \
        list(grants.order_by('filedatetime')
             .values_list('filedatetime', flat=True).distinct())
    # Do not pass go if no grant info available
    if len(grant_dates) == 0:
        return Decimal(0)
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
        grants_per_year = int(Decimal(365) / estimated_day_gap)
    # Now get the latest adjusted shares granted
    latest_grant_date = grant_dates[-1]
    latest_grant_set = grants.filter(filedatetime=latest_grant_date)\
        .values_list('transaction_shares', 'adjustment_factor',
                     'security__conversion_multiple')
    grant_shares_adjusted = Decimal(0)
    for xn_shares, adj_factor, conv_mult in latest_grant_set:
        xn_shares = rep_none_with_zero(xn_shares)
        adj_factor = rep_none_with_zero(adj_factor)
        conv_mult = rep_none_with_zero(conv_mult)
        # print ''
        # print xn_shares, adj_factor, conv_mult
        grant_shares_adjusted += xn_shares * adj_factor * conv_mult
    # Annualize latest grant
    eq_annual_share_grants = grant_shares_adjusted * grants_per_year
    #
    return eq_annual_share_grants


def calc_eq_shares_and_avg_conv_price(issuer, reporting_owner, security,
                                      datetime):
    # This evaluates holdings and conversion prices
    #
    # The reason we pull other ticker securities and exclude consideration
    # of holdings convertible into these securities is that elsewhere in the
    # script, these holdings will be considered on a direct basis, as the
    # script iterates through all tickers.
    #
    # The embedded assumption is that it is better to price a convertible
    # security that trades on an exchange directly rather than on an
    # as-converted basis.
    other_ticker_securities = SecurityPriceHist.objects\
        .filter(issuer=issuer).exclude(security=security)\
        .exclude(security=None)\
        .values_list('security', flat=True)
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .exclude(security__in=other_ticker_securities)\
        .filter(Q(security=security) | Q(underlying_security=security))\
        .exclude(filedatetime__gt=datetime)\
        .exclude(supersededdt__lte=datetime)\
        .values_list('shares_following_xn', 'adjustment_factor',
                     'security__conversion_multiple', 'conversion_price')
    total_eq_shares = Decimal(0)
    conv_price_times_total_eq_shares = Decimal(0)
    for xn_shares, adj_factor, conv_mult, conv_price in holdings:
        # print xn_shares, adj_factor, conv_mult, conv_price
        xn_shares = rep_none_with_zero(xn_shares)
        conv_price = rep_none_with_zero(conv_price)
        total_eq_shares += xn_shares * adj_factor * conv_mult
        conv_price_times_total_eq_shares +=\
            xn_shares * adj_factor * conv_mult * conv_price
    if total_eq_shares == Decimal(0):
        return Decimal(0), Decimal(0)
    else:
        return total_eq_shares,\
            conv_price_times_total_eq_shares / total_eq_shares


def add_secondary_ticker(issuer, reporting_owner, ticker, primary_ticker,
                         prim_share_eqs_held,
                         prim_avg_conv_price,
                         prim_eq_grant_rate,
                         net_xn_shares,
                         prior_prim_share_eqs_held,
                         prior_prim_avg_conv_price,
                         price_dict):
    comb_share_eqs_held = prim_share_eqs_held
    comb_avg_conv_price = prim_avg_conv_price
    comb_eq_grant_rate = prim_eq_grant_rate
    comb_net_xn_shares = net_xn_shares
    prior_comb_share_eqs_held = prior_prim_share_eqs_held
    prior_comb_avg_conv_price = prior_prim_avg_conv_price
    security = ticker.security
    if security is None:
        return comb_share_eqs_held, comb_avg_conv_price,\
            comb_eq_grant_rate, comb_net_xn_shares,\
            prior_comb_share_eqs_held,\
            prior_comb_avg_conv_price

    latest_prim_ticker_price =\
        price_dict[primary_ticker.pk, today]
    latest_sec_ticker_price =\
        price_dict[ticker.pk, today - signal_detect_lookback]

    # If the latest primary ticker price is zero, we ignore
    # the secondary tickers because they can't be sensibly converted
    # to a primary ticker multiple (division by zero).
    # This should probably never happen.

    # Note that this inequality is false if either price is None
    if latest_prim_ticker_price > Decimal(0)\
            and latest_sec_ticker_price > Decimal(0):
        # This is the rate at which we convert units of
        # secondary ticker stock to primary ticker stock
        share_conversion_mult_to_primary_ticker = \
            latest_sec_ticker_price / latest_prim_ticker_price
        sec_share_eqs_held, sec_avg_conv_price =\
            calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                              security, now)
        sec_eq_grant_rate =\
            calc_grants(issuer, reporting_owner, security)

        if sec_share_eqs_held != Decimal(0):
            # Note that numerator omits conversion because units
            # of numerator are in dollars
            total_prim_conv_cost =\
                prim_share_eqs_held * prim_avg_conv_price
            total_sec_conv_cost =\
                sec_share_eqs_held * sec_avg_conv_price

            comb_avg_conv_price = \
                (total_prim_conv_cost + total_sec_conv_cost)\
                / (prim_share_eqs_held + sec_share_eqs_held *
                    share_conversion_mult_to_primary_ticker)
            comb_share_eqs_held = prim_share_eqs_held\
                + sec_share_eqs_held * share_conversion_mult_to_primary_ticker

            comb_eq_grant_rate = prim_eq_grant_rate + sec_eq_grant_rate\
                * share_conversion_mult_to_primary_ticker

    # Now deal with prior lookback data
    prior_prim_ticker_price =\
        price_dict[primary_ticker.pk, today]
    prior_sec_ticker_price =\
        price_dict[ticker.pk, today - signal_detect_lookback]

    if prior_prim_ticker_price > Decimal(0)\
            and prior_sec_ticker_price > Decimal(0):
        prior_share_conversion_mult_to_primary_ticker = \
            prior_sec_ticker_price / prior_prim_ticker_price
        prior_sec_share_eqs_held, prior_sec_avg_conv_price =\
            calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                              security, now +
                                              signal_detect_lookback)

        if prior_sec_share_eqs_held != Decimal(0):
            # Note that numerator omits conversion because units
            # of numerator are in dollars
            prior_total_prim_conv_cost =\
                prior_prim_share_eqs_held * prior_prim_avg_conv_price
            prior_total_sec_conv_cost =\
                prior_sec_share_eqs_held * prior_sec_avg_conv_price

            prior_comb_avg_conv_price = \
                (prior_total_prim_conv_cost + prior_total_sec_conv_cost)\
                / (prior_prim_share_eqs_held + prior_sec_share_eqs_held *
                    prior_share_conversion_mult_to_primary_ticker)
            prior_comb_share_eqs_held = prim_share_eqs_held\
                + prior_sec_share_eqs_held\
                * prior_share_conversion_mult_to_primary_ticker

    comb_net_xn_shares += \
        calc_disc_xn_shares(issuer, reporting_owner, security)

    return comb_share_eqs_held, comb_avg_conv_price, comb_eq_grant_rate,\
        comb_net_xn_shares, prior_comb_share_eqs_held,\
        prior_comb_avg_conv_price


def calc_vals(price_dict):
    print 'Updating values for all affiliations...'
    print '\n'
    # print price_dict
    all_affiliations = Affiliation.objects.all()
    print '   ...adding holding, conversion, grant and behavior attributes...'
    counter = Decimal(0)
    looplength = Decimal(all_affiliations.count())
    for aff in all_affiliations:
        primary_tickers = SecurityPriceHist.objects\
            .filter(issuer=aff.issuer)\
            .filter(primary_ticker_sym=True)
        if primary_tickers.exists():
            sph_obj = primary_tickers[0]
        else:
            sph_obj = None
        # latest share_equivalents_value
        changes = False
        current_price, price_dict = get_price(sph_obj, today, price_dict)
        prior_price, price_dict = get_price(sph_obj,
                                            today - signal_detect_lookback,
                                            price_dict)
        if current_price is not None\
                and aff.share_equivalents_held is not None:
            prior_value = aff.share_equivalents_value
            new_value = aff.share_equivalents_held *\
                max(Decimal(0),
                    (current_price -
                     rep_none_with_zero(aff.average_conversion_price)))
            if prior_value != new_value:
                aff.share_equivalents_value = new_value
                changes = True

        # conversion_to_price_ratio
        if current_price is not None and current_price is not Decimal(0)\
                and aff.average_conversion_price is not None:
            prior_value = aff.average_conversion_price
            new_value =\
                aff.average_conversion_price / current_price
            if prior_value != new_value:
                aff.conversion_to_price_ratio = new_value
                changes = True

        # equity_grant_value
        if current_price is not None\
                and aff.equity_grant_rate is not None:
            prior_value = aff.equity_grant_value
            new_value =\
                aff.equity_grant_rate * current_price
            if prior_value != new_value:
                aff.equity_grant_rate = new_value
                changes = True

        # prior_share_equivalents_value
        if prior_price is not None\
                and aff.prior_share_equivalents_held is not None:
            prior_value = aff.prior_share_equivalents_value
            new_value = aff.prior_share_equivalents_held *\
                max(Decimal(0),
                    (prior_price -
                     rep_none_with_zero(aff.prior_average_conversion_price)))
            if prior_value != new_value:
                aff.prior_share_equivalents_value = new_value
                changes = True

        # prior_conversion_to_price_ratio
        if prior_price is not None and prior_price is not Decimal(0)\
                and aff.prior_average_conversion_price is not None:
            prior_value = aff.prior_average_conversion_price
            new_value =\
                aff.prior_average_conversion_price / prior_price
            if prior_value != new_value:
                aff.prior_conversion_to_price_ratio = new_value
                changes = True

        if changes is True:
            aff.save()
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliations: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n    Done.'
    return


def assemble_pricing_data():
    sph_objs = SecurityPriceHist.objects.all()
    datelist = [today, today - signal_detect_lookback]

    counter = Decimal(0)
    looplength = Decimal(sph_objs.count())
    price_dict = {}
    print '   ...collecting issuer prices...'
    for sph_obj in sph_objs:
        for date in datelist:
            price, price_dict =\
                get_price(sph_obj, date, price_dict)
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s issuers: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    return price_dict


def price_decline(sph_obj, date, timedelta, sp_dict):
    earlier_price, sp_dict =\
        get_price(sph_obj, date, sp_dict)
    later_price, sp_dict =\
        get_price(sph_obj, date + timedelta, sp_dict)
    if earlier_price > later_price:
        return True, sp_dict
    else:
        return False, sp_dict


def price_perf(sph_obj, date, timedelta, sp_dict):
    earlier_price, sp_dict =\
        get_price(sph_obj, date, sp_dict)
    later_price, sp_dict =\
        get_price(sph_obj, date + timedelta, sp_dict)
    if earlier_price is None or later_price is None\
            or earlier_price is Decimal(0):
        return None, sp_dict
    else:
        # print later_price, earlier_price
        return (later_price / earlier_price) - Decimal(1), sp_dict


def post_sale_perf(forms, sph_obj, timedelta, sp_dict):
    perf_l = []
    shares_l = []
    for form in forms:
        xn_price_perf, sp_dict =\
            price_perf(sph_obj, form.transaction_date, timedelta, sp_dict)
        xn_shares = form.transaction_shares
        adj_factor = form.adjustment_factor
        if xn_price_perf is not None\
                and xn_shares is not None:
            perf_l.append(xn_price_perf)
            shares_l.append(xn_shares * adj_factor)
    if len(perf_l) == 1:
        return perf_l[0], sp_dict
    if len(perf_l) > 1:
        post_sale_perf =\
            sum(x * y for x, y in zip(perf_l, shares_l)) / sum(shares_l)
        return post_sale_perf, sp_dict
    else:
        return None, sp_dict


def sale_perf_attributes(issuer, reporting_owner):
    sp_dict = {}
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.exists():
        sph_obj = primary_tickers[0]
    else:
        return
    aff = Affiliation.objects\
        .get(issuer=issuer, reporting_owner=reporting_owner)
    years = [2012, 2013, 2014, 2015]
    test_begin_date = datetime.date(2012, 1, 1)
    month_day_tuples =\
        [[1, 1, 3, 31],
         [4, 1, 6, 30],
         [7, 1, 9, 30],
         [10, 1, 12, 31]]
    regular_sale_forms = \
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(transaction_date__gte=F('filedatetime') +
                datetime.timedelta(-10))\
        .filter(transaction_date__gte=test_begin_date)\
        .exclude(xn_price_per_share=None)\
        .exclude(transaction_shares=None)\
        .filter(transaction_code='S')
    # print 'forms', regular_sale_forms
    td3mo = datetime.timedelta(91)
    td6mo = datetime.timedelta(182)
    td9mo = datetime.timedelta(275)
    td12mo = datetime.timedelta(365)

    quarters_with_sales_since_beg_2012 = 0
    quarter_count_3_mo_decline = 0
    quarter_count_6_mo_decline = 0
    quarter_count_9_mo_decline = 0
    quarter_count_12_mo_decline = 0
    quarters_with_10b_sales_since_beg_2012 = 0
    quarter_count_3_mo_decline_10b = 0
    quarter_count_6_mo_decline_10b = 0
    quarter_count_9_mo_decline_10b = 0
    quarter_count_12_mo_decline_10b = 0

    for year in years:
        for startmonth, startday, endmonth, endday in month_day_tuples:
            startdate = datetime.date(year, startmonth, startday)
            enddate = datetime.date(year, endmonth, endday)
            # print type(startdate), type(enddate)
            period_regular_sales = regular_sale_forms\
                .filter(transaction_date__gte=startdate)\
                .filter(transaction_date__lte=enddate)
            # Regular sales
            # print period_regular_sales
            if period_regular_sales.exists():
                quarters_with_sales_since_beg_2012 += 1

                price_decline_3mo, sp_dict =\
                    price_decline(sph_obj, enddate, td3mo, sp_dict)
                if price_decline_3mo:
                    quarter_count_3_mo_decline += 1

                price_decline_6mo, sp_dict =\
                    price_decline(sph_obj, enddate, td6mo, sp_dict)
                if price_decline_6mo:
                    quarter_count_6_mo_decline += 1

                price_decline_9mo, sp_dict =\
                    price_decline(sph_obj, enddate, td9mo, sp_dict)
                if price_decline_9mo:
                    quarter_count_9_mo_decline += 1

                price_decline_12mo, sp_dict =\
                    price_decline(sph_obj, enddate, td12mo, sp_dict)
                if price_decline_12mo:
                    quarter_count_12_mo_decline += 1
            # 10b5-1 sales
            period_sale_10b_forms =\
                period_regular_sales.exclude(tenbfive_note=None)
            if period_sale_10b_forms.exists():
                quarters_with_10b_sales_since_beg_2012 += 1

                price_decline_3mo, sp_dict =\
                    price_decline(sph_obj, enddate, td3mo, sp_dict)
                if price_decline_3mo:
                    quarter_count_3_mo_decline_10b += 1

                price_decline_6mo, sp_dict =\
                    price_decline(sph_obj, enddate, td6mo, sp_dict)
                if price_decline_6mo:
                    quarter_count_6_mo_decline_10b += 1

                price_decline_9mo, sp_dict =\
                    price_decline(sph_obj, enddate, td9mo, sp_dict)
                if price_decline_9mo:
                    quarter_count_9_mo_decline_10b += 1

                price_decline_12mo, sp_dict =\
                    price_decline(sph_obj, enddate, td12mo, sp_dict)
                if price_decline_12mo:
                    quarter_count_12_mo_decline_10b += 1

    aff.quarters_with_sales_since_beg_2012 =\
        quarters_with_sales_since_beg_2012
    aff.quarter_count_3_mo_decline =\
        quarter_count_3_mo_decline
    aff.quarter_count_6_mo_decline =\
        quarter_count_6_mo_decline
    aff.quarter_count_9_mo_decline =\
        quarter_count_9_mo_decline
    aff.quarter_count_12_mo_decline =\
        quarter_count_12_mo_decline
    aff.quarters_with_10b_sales_since_beg_2012 =\
        quarters_with_10b_sales_since_beg_2012
    aff.quarter_count_3_mo_decline_10b =\
        quarter_count_3_mo_decline_10b
    aff.quarter_count_6_mo_decline_10b =\
        quarter_count_6_mo_decline_10b
    aff.quarter_count_9_mo_decline_10b =\
        quarter_count_9_mo_decline_10b
    aff.quarter_count_12_mo_decline_10b =\
        quarter_count_12_mo_decline_10b

    aff.post_sale_perf_3mo, sp_dict =\
        post_sale_perf(regular_sale_forms, sph_obj, td3mo, sp_dict)
    aff.post_sale_perf_6mo, sp_dict =\
        post_sale_perf(regular_sale_forms, sph_obj, td6mo, sp_dict)
    aff.post_sale_perf_9mo, sp_dict =\
        post_sale_perf(regular_sale_forms, sph_obj, td9mo, sp_dict)
    aff.post_sale_perf_12mo, sp_dict =\
        post_sale_perf(regular_sale_forms, sph_obj, td12mo, sp_dict)
    period_sale_10b_forms =\
        regular_sale_forms.exclude(tenbfive_note=None)
    aff.post_sale_perf_10b_3mo, sp_dict =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td3mo, sp_dict)
    aff.post_sale_perf_10b_6mo, sp_dict =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td6mo, sp_dict)
    aff.post_sale_perf_10b_9mo, sp_dict =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td9mo, sp_dict)
    aff.post_sale_perf_10b_12mo, sp_dict =\
        post_sale_perf(period_sale_10b_forms, sph_obj, td12mo, sp_dict)

    td_since_begin = today - test_begin_date
    cumulativeperformance, sp_dict =\
        price_perf(sph_obj, test_begin_date,
                   td_since_begin, sp_dict)
    years_since_begin = Decimal(td_since_begin.days) / Decimal(365)
    if cumulativeperformance is not None:
        aff.annualized_perf_from_beg_2012_to_today =\
            (cumulativeperformance +
             Decimal(1))**(Decimal(1)/years_since_begin)\
            - Decimal(1)
    aff.save()
    return


def calc_holdings(aff, issuer, reporting_owner, sec_ids, primary_sec_id, date,
                  price_dict):

    ticker_list = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None).values_list('security', 'pk')
    ticker_sec_dict = dict(ticker_list)
    prim_price = get_price(ticker_sec_dict[primary_sec_id],
                           date, price_dict)
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security__in=sec_ids) |
                Q(underlying_security__in=sec_ids))\
        .exclude(filedatetime__gt=datetime)\
        .exclude(supersededdt__lte=datetime)\
        .exclude(shares_following_xn=None)\
        .exclude(security=None)\
        .values('shares_following_xn', 'adjustment_factor',
                'security__conversion_multiple', 'conversion_price',
                'security', 'underlying_security')
    total_shares_held = Decimal(0)
    total_value = Decimal(0)
    total_conv_cost = Decimal(0)
    for h in holdings:
        if h['security'] != primary_sec_id and\
                h['underlying_security'] != primary_sec_id:

            holding_price = get_price(ticker_sec_dict[h['security']],
                                      date, price_dict)
            share_conversion_mult_to_primary_ticker = \
                holding_price / prim_price
        else:
            share_conversion_mult_to_primary_ticker = Decimal(1)
        security_shares = h['shares_following_xn'] * h['adjustment_factor'] *\
            h['security__conversion_multiple']
        prim_eq_shares = security_shares *\
            share_conversion_mult_to_primary_ticker

        price = get_price(ticker_sec_dict[h['security']], date, price_dict)
        adj_conversion_price = rep_none_with_zero(h['conversion_price']) /\
            h['adjustment_factor']
        holding_value = security_shares *\
            max(Decimal(0), price - adj_conversion_price)
        conv_cost = adj_conversion_price * security_shares
        total_shares_held += prim_eq_shares
        total_value += holding_value
        total_conv_cost += conv_cost
    avg_conv_price = total_conv_cost / total_shares_held

    return total_shares_held, avg_conv_price, total_value




def calc_person_affiliation(issuer, reporting_owner, price_dict):
    affiliation_forms = Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(reporting_owner_cik=reporting_owner)
    latest_form = affiliation_forms.latest('filedatetime')
    aff =\
        Affiliation.objects.get(issuer=issuer,
                                reporting_owner=reporting_owner)
    aff.issuer_name = IssuerCIK.objects.get(cik_num=issuer).name
    aff.person_name = latest_form.reporting_owner_name
    aff.is_director = latest_form.is_director
    aff.is_officer = latest_form.is_officer
    aff.is_ten_percent = latest_form.is_ten_percent
    aff.is_something_else = latest_form.is_something_else
    aff.reporting_owner_title = latest_form.reporting_owner_title
    aff.latest_form_dt = latest_form.filedatetime
    aff.is_active = True
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.count() == 0:
        aff.save()
        return
    prim_ticker = primary_tickers[0]
    prim_security = prim_ticker.security
    all_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .exclude(security=None)
    ticker_sec_ids = all_tickers.values_list('security', flat=True)
    calc_holdings(issuer, reporting_owner, ticker_sec_ids, prim_security.pk,
                  today)



    other_ticker_securities = SecurityPriceHist.objects\
        .filter(issuer=issuer).exclude(security=security)\
        .exclude(security=None)\
        .values_list('security', flat=True)
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .exclude(security__in=other_ticker_securities)\
        .filter(Q(security=security) | Q(underlying_security=security))\
        .exclude(filedatetime__gt=datetime)\
        .exclude(supersededdt__lte=datetime)\
        .values_list('shares_following_xn', 'adjustment_factor',
                     'security__conversion_multiple', 'conversion_price')
    total_eq_shares = Decimal(0)
    conv_price_times_total_eq_shares = Decimal(0)
    for xn_shares, adj_factor, conv_mult, conv_price in holdings:
        # print xn_shares, adj_factor, conv_mult, conv_price
        xn_shares = rep_none_with_zero(xn_shares)
        conv_price = rep_none_with_zero(conv_price)
        total_eq_shares += xn_shares * adj_factor * conv_mult
        conv_price_times_total_eq_shares +=\
            xn_shares * adj_factor * conv_mult * conv_price
    if total_eq_shares == Decimal(0):
        return Decimal(0), Decimal(0)
    else:
        return total_eq_shares,\
            conv_price_times_total_eq_shares / total_eq_shares




def get_new_affiliation_form_data(issuer_and_rep_owner_list):

    counter = 0.0
    looplength = float(len(issuer_and_rep_owner_list))
    price_dict = assemble_pricing_data()
    for issuer, reporting_owner in issuer_and_rep_owner_list:
        price_dict =\
            calc_person_affiliation(issuer, reporting_owner, price_dict)


        affiliation_forms = Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(reporting_owner_cik=reporting_owner)
        latest_form = affiliation_forms.latest('filedatetime')
        affiliation =\
            Affiliation.objects.get(issuer=issuer,
                                    reporting_owner=reporting_owner)

        affiliation.issuer_name = IssuerCIK.objects.get(cik_num=issuer).name
        affiliation.person_name = latest_form.reporting_owner_name
        affiliation.is_director = latest_form.is_director
        affiliation.is_officer = latest_form.is_officer
        affiliation.is_ten_percent = latest_form.is_ten_percent
        affiliation.is_something_else = latest_form.is_something_else
        affiliation.reporting_owner_title = latest_form.reporting_owner_title
        affiliation.latest_form_dt = latest_form.filedatetime
        affiliation.is_active = True
        primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
            .filter(primary_ticker_sym=True)

        if primary_tickers.exists():
            primary_ticker = primary_tickers[0]
            primary_security = primary_ticker.security

            share_equivalents_held, average_conversion_price =\
                calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                                  primary_security, now)
            prior_share_equivalents_held, prior_average_conversion_price =\
                calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                                  primary_security, now +
                                                  signal_detect_lookback)
            net_xn_shares = \
                calc_disc_xn_shares(issuer, reporting_owner, primary_security)
            equity_grant_rate =\
                calc_grants(issuer, reporting_owner, primary_security)
            other_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
                .filter(primary_ticker_sym=False)
            # See if any other tickers have useful data
            for ticker in other_tickers:
                share_equivalents_held, average_conversion_price,\
                    equity_grant_rate, net_xn_shares,\
                    prior_share_equivalents_held,\
                    prior_average_conversion_price =\
                    add_secondary_ticker(issuer, reporting_owner, ticker,
                                         primary_ticker,
                                         share_equivalents_held,
                                         average_conversion_price,
                                         equity_grant_rate,
                                         net_xn_shares,
                                         prior_share_equivalents_held,
                                         prior_average_conversion_price,
                                         price_dict)

            # Placeholder behavior calculation
            # print '\n net_xn_shares', net_xn_shares, equity_grant_rate
            if net_xn_shares > Decimal(0):
                behavior = buyer
                # print 'buyer'
            elif net_xn_shares == Decimal(0):
                behavior = None
                # print 'none'
            elif equity_grant_rate is not None\
                    and Decimal(-1) * net_xn_shares <= equity_grant_rate:
                behavior = None
                # print 'none bc /eq grants'
            else:
                behavior = seller
                # print 'seller'

            affiliation.share_equivalents_held = share_equivalents_held
            affiliation.average_conversion_price = average_conversion_price
            affiliation.equity_grant_rate = equity_grant_rate
            affiliation.behavior = behavior
            affiliation.prior_share_equivalents_held =\
                prior_share_equivalents_held
            if prior_share_equivalents_held >= 1000000000000\
                    or share_equivalents_held >= 1000000000000:
                affiliation.prior_share_equivalents_held = 0
                affiliation.share_equivalents_held = 0
                print issuer, reporting_owner, affiliation.person_name
                print 'prior_share_equivalents_held',
                print prior_share_equivalents_held
                print 'share_equivalents_held',
                print share_equivalents_held
                print 'a number is too big'

            affiliation.prior_average_conversion_price =\
                prior_average_conversion_price

        # HOW THE ABOVE WORKS:
        #    If stock has just a primary ticker, use that one,
        #    if stock has secondary tickers figure out latest price multiplier
        #       as to primary ticker
        #       adds converted equivalent shares of secondary to primary
        #       ticker using multiplier
        #       Also converts conversion prices, equity grant rates

        affiliation.save()
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliation to update: %.2f%%" %
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

    calc_vals(price_dict)

    return


def update(affiliations_with_new_forms):
    print 'Updating affiliations with new form data...'
    get_new_affiliation_form_data(affiliations_with_new_forms)
    print '\n    Done.'
    return


def replace():
    print 'Updating all affiliation data...'
    affiliations_with_new_forms = Affiliation.objects.all()\
        .values_list('issuer', 'reporting_owner')
    get_new_affiliation_form_data(affiliations_with_new_forms)
    print '\n    Done.'
    return


def annotatestats():
    affiliations = Affiliation.objects.all()\
        .values_list('issuer', 'reporting_owner')
    affiliations.update(
        quarters_with_sales_since_beg_2012=None,
        quarter_count_3_mo_decline=None,
        quarter_count_6_mo_decline=None,
        quarter_count_9_mo_decline=None,
        quarter_count_12_mo_decline=None,
        post_sale_perf_3mo=None,
        post_sale_perf_6mo=None,
        post_sale_perf_9mo=None,
        post_sale_perf_12mo=None,
        quarters_with_10b_sales_since_beg_2012=None,
        quarter_count_3_mo_decline_10b=None,
        quarter_count_6_mo_decline_10b=None,
        quarter_count_9_mo_decline_10b=None,
        quarter_count_12_mo_decline_10b=None,
        post_sale_perf_10b_3mo=None,
        post_sale_perf_10b_6mo=None,
        post_sale_perf_10b_9mo=None,
        post_sale_perf_10b_12mo=None,
        annualized_perf_from_beg_2012_to_today=None,
    )
    counter = 0.0
    looplength = float(len(affiliations))
    for issuer, reporting_owner in affiliations:
        top_holders = Affiliation.objects.filter(issuer=issuer)\
            .order_by('-share_equivalents_value')\
            .values_list('reporting_owner', flat=True)
        top_3_holders = list(top_holders)[:3]
        if reporting_owner in top_3_holders:
            sale_perf_attributes(issuer, reporting_owner)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliation to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
        # django.db.reset_queries()
    return
