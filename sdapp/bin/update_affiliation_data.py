import datetime
from decimal import Decimal
import sys

from django.db.models import Q

from sdapp.bin.globals import today, todaymid
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


def replace_none_with_zero(inputvar):
    if inputvar is not None:
        return inputvar
    else:
        return Decimal(0)


def laxer_start_price(sec_price_hist, today):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__gte=today-wkd_td)\
        .filter(close_date__lte=today).order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_price(issuer, today):
    primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if primary_tickers.exists():
        sec_price_hist = primary_tickers[0]
    else:
        return None
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=today)
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        laxer_price = laxer_start_price(sec_price_hist, today)
        return laxer_price


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
        return None
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
        xn_shares = replace_none_with_zero(xn_shares)
        adj_factor = replace_none_with_zero(adj_factor)
        conv_mult = replace_none_with_zero(conv_mult)
        # print ''
        # print xn_shares, adj_factor, conv_mult
        grant_shares_adjusted += xn_shares * adj_factor * conv_mult
    # Annualize latest grant
    eq_annual_share_grants = grant_shares_adjusted * grants_per_year
    #
    return eq_annual_share_grants


def calc_eq_shares_and_avg_conv_price(issuer, reporting_owner, security):
    holdings = Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_owner)\
        .filter(Q(security=security) | Q(underlying_security=security))\
        .filter(supersededdt=None)\
        .values_list('transaction_shares', 'adjustment_factor',
                     'security__conversion_multiple', 'conversion_price')
    total_eq_shares = Decimal(0)
    conv_price_times_total_eq_shares = Decimal(0)
    for xn_shares, adj_factor, conv_mult, conv_price in holdings:
        # print xn_shares, adj_factor, conv_mult, conv_price
        xn_shares = replace_none_with_zero(xn_shares)
        conv_price = replace_none_with_zero(conv_price)
        total_eq_shares += xn_shares * adj_factor * conv_mult
        conv_price_times_total_eq_shares +=\
            xn_shares * adj_factor * conv_mult * conv_price
    if total_eq_shares == Decimal(0):
        return Decimal(0), None
    else:
        return total_eq_shares,\
            conv_price_times_total_eq_shares / total_eq_shares


def add_secondary_ticker(issuer, reporting_owner, ticker, primary_ticker,
                         share_equivalents_held,
                         average_conversion_price, equity_grant_rate):
    security = ticker.security
    primary_ticker_close_prices =\
        ClosePrice.objects.filter(securitypricehist=primary_ticker)
    ticker_close_prices =\
        ClosePrice.objects.filter(securitypricehist=ticker)
    if primary_ticker_close_prices.exists()\
            and ticker_close_prices.exists():
        latest_primary_ticker_price =\
            primary_ticker_close_prices.latest('close_date')
        latest_ticker_price =\
            ticker_close_prices.latest('close_date')
        # This is the rate at which we convert units of
        # secondary ticker stock to primary ticker stock
        conversion_from_ticker_to_primary_ticker = \
            latest_ticker_price / latest_primary_ticker_price
        share_eqs_held, avg_conv_price =\
            calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                              security)
        eq_grant_rate =\
            calc_grants(issuer, reporting_owner, security)
        if share_eqs_held != Decimal(0)\
                and conversion_from_ticker_to_primary_ticker is not None:
            # Note that numerator omits conversion -- conv factors cancel
            # out when converting shares times conv_price to primary
            average_conversion_price = \
                (share_equivalents_held * average_conversion_price
                 + (share_eqs_held * avg_conv_price))\
                / (share_equivalents_held + share_eqs_held
                    * conversion_from_ticker_to_primary_ticker)
            share_equivalents_held += share_eqs_held\
                * conversion_from_ticker_to_primary_ticker
        if eq_grant_rate is not None:
            equity_grant_rate += eq_grant_rate\
                * conversion_from_ticker_to_primary_ticker

    return share_equivalents_held, average_conversion_price,\
        equity_grant_rate


def get_new_affiliation_form_data(issuer_and_rep_owner_list):
    counter = 0.0
    looplength = float(len(issuer_and_rep_owner_list))
    for issuer, reporting_owner in issuer_and_rep_owner_list:
        affiliation_forms = Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(reporting_owner_cik=reporting_owner)
        latest_form = affiliation_forms.latest('filedatetime')
        affiliation =\
            Affiliation.objects.get(issuer=issuer,
                                    reporting_owner=reporting_owner)

        affiliation.person_name = latest_form.reporting_owner_name
        affiliation.is_director = latest_form.is_director
        affiliation.is_officer = latest_form.is_officer
        affiliation.is_ten_percent = latest_form.is_ten_percent
        affiliation.is_something_else = latest_form.is_something_else
        affiliation.reporting_owner_title = latest_form.reporting_owner_title
        affiliation.latest_form_dt = latest_form.filedatetime

        primary_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
            .filter(primary_ticker_sym=True)
        if primary_tickers.exists():
            primary_ticker = primary_tickers[0]
            primary_security = primary_ticker.security

            share_equivalents_held, average_conversion_price =\
                calc_eq_shares_and_avg_conv_price(issuer, reporting_owner,
                                                  primary_security)
            equity_grant_rate =\
                calc_grants(issuer, reporting_owner, primary_security)
            other_tickers = SecurityPriceHist.objects.filter(issuer=issuer)\
                .filter(primary_ticker_sym=False)
            # See if any other tickers have useful data
            for ticker in other_tickers:
                share_equivalents_held, average_conversion_price,\
                    equity_grant_rate =\
                    add_secondary_ticker(issuer, reporting_owner, ticker,
                                         primary_ticker,
                                         share_equivalents_held,
                                         average_conversion_price,
                                         equity_grant_rate)

        # HOW THE ABOVE WORKS:
        #    If stock has just a primary ticker, use that one,
        #    if stock has secondary tickers figure out latest price multiplier
        #       as to primary ticker
        #       adds converted equivalent shares of secondary to primary
        #       ticker using multiplier
        #       Also converts conversion prices, equity grant rates
        else:
            share_equivalents_held, average_conversion_price,\
                equity_grant_rate = None, None, None
        affiliation.share_equivalents_held = share_equivalents_held
        affiliation.average_conversion_price = average_conversion_price
        affiliation.equity_grant_rate = equity_grant_rate
        affiliation.save()
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s affiliation to update: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    return


def calc_percentiles():
    print 'Updating percentiles for all affiliations...'

    price_dict = {}
    issuers = IssuerCIK.objects.all().values_list('cik_num', flat=True)
    counter = Decimal(0)
    looplength = Decimal(issuers.count())
    print '   ...collecting issuer prices...'
    for issuer in issuers:
        price_dict[issuer] = get_price(issuer, today)
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s issuer prices: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n'
    # print price_dict
    all_affiliations = Affiliation.objects.all()
    print '   ...adding holding, conversion and grant value attributes...'
    counter = Decimal(0)
    looplength = Decimal(all_affiliations.count())
    for affiliation in all_affiliations:
        # share_equivalents_value
        changes = False
        if affiliation.share_equivalents_held is None\
                or price_dict[affiliation.issuer.pk] is None:
            affiliation.share_equivalents_value = None
        else:
            affiliation.share_equivalents_value =\
                affiliation.share_equivalents_held *\
                price_dict[affiliation.issuer.pk]
            changes = True
        # conversion_to_price_ratio
        if affiliation.average_conversion_price is None\
                or price_dict[affiliation.issuer.pk] is None:
            affiliation.conversion_to_price_ratio = None
        else:
            affiliation.conversion_to_price_ratio =\
                affiliation.average_conversion_price /\
                price_dict[affiliation.issuer.pk]
            changes = True
        # equity_grant_value
        if affiliation.equity_grant_rate is None\
                or price_dict[affiliation.issuer.pk] is None:
            affiliation.equity_grant_value = None
        else:
            affiliation.equity_grant_value =\
                affiliation.equity_grant_rate *\
                price_dict[affiliation.issuer.pk]
            changes = True
        # print affiliation.share_equivalents_value, affiliation.conversion_to_price_ratio, affiliation.equity_grant_rate
        if changes is True:
            affiliation.save()
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s ratios: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n'

    print '   ...updating percentiles for inactive affiliations...'
    # Inactive affiliations are those that have no activity for a year
    # and also are at zero share equivalents held.
    start_dt = todaymid - datetime.timedelta(365)
    Affiliation.objects.exclude(latest_form_dt__gte=start_dt)\
        .exclude(share_equivalents_value__gt=Decimal(0))\
        .update(share_equivalents_value=None,
                average_conversion_price_ratio_percentile=None,
                equity_grant_value_percentile=None)
    print '   ...now handling active affiliations...'
    # Active affiliations
    active_affiliations = Affiliation.objects\
        .filter(Q(share_equivalents_value__gt=Decimal(0))
                | Q(latest_form_dt__gte=start_dt))

    # average_conversion_price_ratio_percentile
    print '   ...adding conversion_to_price_ratio percentiles...'
    affiliations_ordered_by_conv_price_ratio =\
        active_affiliations.exclude(conversion_to_price_ratio=None)\
        .order_by('conversion_to_price_ratio')
    last_percentile = Decimal(0)
    last_value = Decimal(0)
    counter = Decimal(0)
    looplength = Decimal(affiliations_ordered_by_conv_price_ratio.count())
    for a in affiliations_ordered_by_conv_price_ratio:
        if a.conversion_to_price_ratio == last_value:
            a.average_conversion_price_ratio_percentile =\
                last_percentile
            a.save()
        else:
            a.average_conversion_price_ratio_percentile =\
                counter / looplength * Decimal(100)
            last_percentile = a.average_conversion_price_ratio_percentile
            last_value = a.conversion_to_price_ratio
            a.save()
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s conv. price ratio percentiles: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n'
    # share_equivalents_value_percentile
    print '   ...adding share_equivalents_value percentiles...'
    affiliations_ordered_by_share_equivalents_value =\
        active_affiliations.exclude(share_equivalents_value=None)\
        .order_by('share_equivalents_value')
    last_percentile = Decimal(0)
    last_value = Decimal(0)
    counter = Decimal(0)
    looplength =\
        Decimal(affiliations_ordered_by_share_equivalents_value.count())
    for a in affiliations_ordered_by_share_equivalents_value:
        if a.share_equivalents_value == last_value:
            a.share_equivalents_value_percentile =\
                last_percentile
            a.save()
        else:
            a.share_equivalents_value_percentile =\
                counter / looplength * Decimal(100)
            last_percentile = a.share_equivalents_value_percentile
            last_value = a.share_equivalents_value
            a.save()
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s share equiv. held percentiles: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n'
    # equity_grant_value_percentile
    print '   ...adding equity_grant_value percentiles...'
    affiliations_ordered_by_equity_grant_value =\
        Affiliation.objects.exclude(equity_grant_value=None)\
        .order_by('equity_grant_value')
    last_percentile = Decimal(0)
    last_value = Decimal(0)
    counter = Decimal(0)
    looplength =\
        Decimal(affiliations_ordered_by_equity_grant_value.count())
    for a in affiliations_ordered_by_equity_grant_value:
        if a.equity_grant_value == last_value:
            a.equity_grant_value_percentile =\
                last_percentile
            a.save()
        else:
            a.equity_grant_value_percentile =\
                counter / looplength * Decimal(100)
            last_percentile = a.equity_grant_value_percentile
            last_value = a.equity_grant_value
            a.save()
        counter += Decimal(1)
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s equity grant rate percentiles: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()

    print '\n    Done.'
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
