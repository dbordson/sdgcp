import datetime
from decimal import Decimal
import pytz
import sys

import django.db
from django.db.models import F, Q, Sum

from sdapp.models import (Affiliation, DiscretionaryXnEvent, Form345Entry,
                          PersonSignal, SecurityPriceHist, ClosePrice,
                          SigDisplay, WatchedName)
# from sdapp.models import WatchedName
from sdapp.bin.globals import (abs_sig_min, big_xn_amt, buy,
                               buy_response_to_perf, date_of_any_new_filings,
                               perf_period_days_td, rel_sig_min,
                               recent_sale_period, sell, sell_response_to_perf,
                               seller, signal_detect_lookback,
                               significant_stock_move, hist_sale_period,
                               today, todaymid)

from sdapp.bin.sdapptools import laxer_start_price, calc_perf
# from sdapp.bin.update_affiliation_data import calc_grants


def appendif(startlist, newitem):
    if newitem is None:
        return startlist
    else:
        startlist.append(newitem)
        return startlist


def get_price(sec_price_hist, date, issuer, hist_price_dict):
    if (issuer, date) in hist_price_dict:
        return hist_price_dict[issuer, date]
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date)
    if close_price.exists():
        hist_price_dict[issuer, date] = close_price[0].adj_close_price
        return close_price[0].adj_close_price
    else:
        laxer_price = laxer_start_price(sec_price_hist, date)
        hist_price_dict[issuer, date] = laxer_price
        return laxer_price


def calc_holdings(securities, issuer, reporting_person, hist_price_dict):
    first_filing_date = securities[0][3]
    EST = pytz.timezone('America/New_York')
    ffd = first_filing_date
    first_filing_dt =\
        datetime.datetime(ffd.year, ffd.month, ffd.day,
                          0, 0, 0, 0, tzinfo=EST)\
        + datetime.timedelta(1)
    ticker_securities = SecurityPriceHist.objects\
        .filter(issuer=issuer, primary_ticker_sym=True)
    if ticker_securities.exists():
        ticker_security = ticker_securities[0].security
        stock_price_for_holdings =\
            get_price(ticker_securities[0], ffd, issuer, hist_price_dict)
    else:
        # No value if can't find a ticker for pricing.
        return None
    if stock_price_for_holdings is None:
        return None
    person_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_person)\
        .filter(Q(supersededdt__gt=first_filing_dt) |
                Q(supersededdt=None))\
        .exclude(filedatetime__gt=first_filing_dt)
    stock_values = person_forms\
        .filter(security=ticker_security)\
        .exclude(reported_shares_following_xn=None)\
        .values_list('shares_following_xn', 'adjustment_factor',
                     'conversion_price')
    stock_deriv_values = person_forms\
        .filter(underlying_security=ticker_security)\
        .exclude(underlying_shares=None)\
        .values_list('underlying_shares', 'adjustment_factor',
                     'conversion_price')
    all_values = list(stock_values) + list(stock_deriv_values)
    prior_holding_value = Decimal(0)
    for rep_shares, adj_factor, conversion_price in all_values:
        if conversion_price is None:
            cp = Decimal(0)
        else:
            cp = conversion_price
        prior_holding_value += Decimal(rep_shares) * Decimal(adj_factor)\
            * max(0, stock_price_for_holdings - cp)
    #
    return prior_holding_value


def is_ceo(person_title_list):
    keywords = ['ceo', 'chief executive officer',
                'principal executive officer']
    ceo_match = False
    for person_title in person_title_list:
        if person_title is not None:
            lowercase_title = person_title.lower()
            for keyword in keywords:
                if lowercase_title in keyword:
                    ceo_match = True
    return ceo_match


def create_disc_xn_events():
    #
    print 'Creating new discretionary transaction objects'
    print '    sorting...'
    #
    existing_sig_pks =\
        DiscretionaryXnEvent.objects.values_list('form_entry__pk')
    #
    # Note that the below contains an 'F Object'; since this may be unfamiliar,
    # I will explain -- it filters for transaction dates that are greater than
    # 5 days (timedelta) before the filedatetime.  This avoids interpreting an
    # old transaction in a newly filed form as a new signal.
    #

    # equity_securities = SecurityPriceHist.objects\
    #     .filter(issuer=issuer).values_list('security', flat=True)
    # a = Form345Entry.objects\
    #     .filter(transaction_date__gte=F('filedatetime') +
    #             datetime.timedelta(-10))\
    #     .filter(filedatetime__gte=todaymid)\
    #     .filter(Q(security__in=equity_securities) |
    #             (Q(underlying_security__in=equity_securities) & ~
    #              Q(security__in=equity_securities)))

    a = Form345Entry.objects\
        .filter(filedatetime__gte=todaymid - hist_sale_period)\
        .filter(transaction_date__gte=F('filedatetime') +
                datetime.timedelta(-10))\
        .exclude(transaction_date=None)\
        .exclude(xn_price_per_share=None)\
        .exclude(transaction_shares=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
        .exclude(pk__in=existing_sig_pks)
    newxns = []
    print '    interpreting...'
    counter = 0.0
    looplength = float(len(a))
    for item in a:
        if item.xn_acq_disp_code == 'D':
            sign_transaction_shares = \
                Decimal(-1) * item.transaction_shares * item.adjustment_factor\
                * item.security.conversion_multiple
            xn_val = item.xn_price_per_share * sign_transaction_shares
        else:
            sign_transaction_shares = \
                item.transaction_shares * item.adjustment_factor\
                * item.security.conversion_multiple
            xn_val = item.xn_price_per_share * sign_transaction_shares
        newxn =\
            DiscretionaryXnEvent(issuer=item.issuer_cik,
                                 reporting_person=item.reporting_owner_cik,
                                 person_title=item.reporting_owner_title,
                                 security=item.security,
                                 form_entry_id=item.pk,
                                 xn_acq_disp_code=item.xn_acq_disp_code,
                                 transaction_code=item.transaction_code,
                                 xn_val=xn_val,
                                 xn_shares=sign_transaction_shares,
                                 filedate=item.filedatetime.date())
        newxns.append(newxn)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s transaction events to add: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    #
    print '\n    saving any new...'
    DiscretionaryXnEvent.objects.bulk_create(newxns)
    #
    print 'done.\n'
    django.db.reset_queries()
    return


def replace_person_signals():
    print 'Replacing PersonSignal objects'
    print '    sorting...'
    a =\
        DiscretionaryXnEvent.objects\
        .filter(filedate__gte=today - signal_detect_lookback)\
        .values_list('reporting_person', 'issuer').distinct()
    newpersonsignals = []
    print '    interpreting...'
    counter = 0.0
    looplength = float(len(a))
    hist_price_dict = {}
    for reporting_person, issuer in a:
        # When primary ticker concept is added, adjust filter accordingly.
        aff_events = DiscretionaryXnEvent.objects.filter(issuer=issuer)\
            .filter(reporting_person=reporting_person)\
            .filter(filedate__gte=today - signal_detect_lookback)
        sec_price_hists = SecurityPriceHist.objects.filter(issuer=issuer)\
            .filter(primary_ticker_sym=True)\
            .order_by('security__short_sec_title')
        if sec_price_hists.exists():
            sec_price_hist = sec_price_hists[0]
            security = sec_price_hist.security
        else:
            sec_price_hist = None
            security = None
        reporting_person_title = aff_events.latest('filedate').person_title
        #
        securities = aff_events.order_by('filedate')\
            .values_list('security', 'xn_val', 'xn_shares', 'filedate')
        #
        entryfiledates = list(aff_events.order_by('filedate')
                              .order_by('filedate')
                              .values_list('filedate', flat=True))
        first_file_date = entryfiledates[0]
        last_file_date = entryfiledates[-1]
        transactions = len(entryfiledates)
        #
        # eq_annual_share_grants =\
        #    calc_grants(issuer, reporting_person, security)
        # THE BELOW NEEDS TO BE FIXED -- ASSUMES EQUITY GRANTS ARE ZERO
        # PLACEHOLDER HERE BECAUSE CALC MAY BE OBVIATED ONCE NEW
        # update_affiliation_data script is done
        eq_annual_share_grants =\
            Decimal(0)
        #
        # Get holdings before form filed
        prior_holding_value =\
            calc_holdings(securities, issuer, reporting_person,
                          hist_price_dict)
        securities_dict = {}
        net_signal_value = Decimal(0)
        net_signal_shares = Decimal(0)
        gross_acq_value = Decimal(0)
        gross_disp_value = Decimal(0)
        #
        # Find primary securities and set up shares transacted
        # by filedate
        filedate_dict = {}
        for security, xn_val, xn_shares, filedate in securities:
            # Is the transaction security in the tracking dict object?
            # If so, add to existing key; if not, add a dict key for it.
            if security in securities_dict:
                securities_dict[security][0] += xn_val
                securities_dict[security][1] += xn_shares
            else:
                securities_dict[security] = [xn_val, xn_shares]
            if filedate in filedate_dict:
                filedate_dict[filedate][0] += xn_val
                filedate_dict[filedate][1] += xn_shares
            else:
                filedate_dict[filedate] = [xn_val, xn_shares]
            #
            net_signal_value += xn_val
            net_signal_shares += xn_shares
            #
            if xn_val > 0:
                gross_acq_value += xn_val
            else:
                gross_disp_value += xn_val
        #
        signal_detect_date = None
        net_val_of_date = Decimal(0)
        net_shares_of_date = Decimal(0)
        # Find the date activity became significant.
        significant = False
        for filedate, [net_xn_value, net_xn_shares] in\
                sorted(filedate_dict.iteritems()):
            net_val_of_date += net_xn_value
            net_shares_of_date += net_xn_shares
            # This tests if the transactions to date are significant
            # and if so and if the signal was not yet detected, it sets the
            # date of detection.
            if prior_holding_value is not None\
                    and prior_holding_value > Decimal(0)\
                    and abs(net_val_of_date) >= abs_sig_min\
                    and (abs(net_val_of_date) / prior_holding_value >=
                         rel_sig_min or abs(net_val_of_date) >= big_xn_amt)\
                    and signal_detect_date is None:
                if net_signal_value < Decimal(0)\
                        and abs(net_shares_of_date) > eq_annual_share_grants:
                    signal_detect_date = filedate
                    significant = True
                elif net_signal_value >= Decimal(0):
                    signal_detect_date = filedate
                    significant = True
        #
        # This fills in the last transaction date if signal is not significant.
        if signal_detect_date is None:
            signal_detect_date = last_file_date
        # Function checks if stock price stored in RAM; otherwise call from DB.
        stock_price_for_perf_lookback =\
            get_price(sec_price_hist, filedate - perf_period_days_td,
                      issuer, hist_price_dict)
        stock_price_at_detection =\
            get_price(sec_price_hist, filedate, issuer, hist_price_dict)
        stock_price_now =\
            get_price(sec_price_hist, today, issuer, hist_price_dict)
        #
        preceding_stock_perf =\
            calc_perf(stock_price_at_detection, stock_price_for_perf_lookback)
        perf_after_detection =\
            calc_perf(stock_price_now, stock_price_at_detection)
        subs_stock_period_days = (todaymid.date() - signal_detect_date).days
        #
        # This determines the gross signal value whether a net buy or sale
        if gross_acq_value >= Decimal(-1) * gross_disp_value:
            gross_signal_value = gross_acq_value
        else:
            gross_signal_value = gross_disp_value
        # This assigns the signal anme
        if gross_signal_value >= 0:
            if preceding_stock_perf is not None\
                    and preceding_stock_perf < -significant_stock_move:
                signal_name = buy_response_to_perf
            else:
                signal_name = buy
        else:
            if preceding_stock_perf is not None\
                    and preceding_stock_perf > significant_stock_move:
                signal_name = sell_response_to_perf
            else:
                signal_name = sell
        #
        security_1 = max(securities_dict, key=securities_dict.get)
        if securities_dict[security_1][1] == Decimal(0)\
                or securities_dict[security_1][1] is None:
            average_price_sec_1 = None
        else:
            average_price_sec_1 =\
                securities_dict[security_1][0] / securities_dict[security_1][1]
        if prior_holding_value == Decimal(0) or prior_holding_value is None:
            net_signal_pct = None
        else:
            net_signal_pct = abs(net_signal_value) / prior_holding_value\
                * Decimal(100)

        if len(securities_dict) == 1:
            only_security_1 = True
        else:
            only_security_1 = False
        #
        newpersonsignals.append(
            PersonSignal(issuer_id=issuer,
                         sec_price_hist=sec_price_hist,
                         reporting_person_id=reporting_person,
                         eq_annual_share_grants=eq_annual_share_grants,
                         security_1_id=security_1,
                         only_security_1=only_security_1,
                         reporting_person_title=reporting_person_title,
                         signal_name=signal_name,
                         signal_detect_date=signal_detect_date,
                         first_file_date=first_file_date,
                         last_file_date=last_file_date,
                         transactions=transactions,
                         average_price_sec_1=average_price_sec_1,
                         gross_signal_value=gross_signal_value,
                         net_signal_value=net_signal_value,
                         net_signal_shares=net_signal_shares,
                         prior_holding_value=prior_holding_value,
                         net_signal_pct=net_signal_pct,
                         preceding_stock_perf=preceding_stock_perf,
                         perf_period_days=perf_period_days_td.days,
                         perf_after_detection=perf_after_detection,
                         subs_stock_period_days=subs_stock_period_days,
                         significant=significant,
                         new=True))
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s person signals to add: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n    deleting old and saving...'
    PersonSignal.objects.all().delete()
    PersonSignal.objects.bulk_create(newpersonsignals)
    print 'done.'
    django.db.reset_queries()
    print ''
    return


def agg_selling_activity(issuer, startdate, enddate):
    issuer_sale_xns =\
        DiscretionaryXnEvent.objects.filter(issuer=issuer)\
        .filter(xn_acq_disp_code='D')\
        .filter(filedate__gt=startdate)\
        .filter(filedate__lte=enddate)
    if not issuer_sale_xns.exists():
        return Decimal(0), Decimal(0)
    sph_qs = SecurityPriceHist.objects.filter(issuer=issuer)\
        .filter(primary_ticker_sym=True)
    if sph_qs.exists() and sph_qs[0].security is not None:
        prim_sph_obj = sph_qs[0]
        prim_sec = prim_sph_obj.security
        number_of_shares_sold =\
            issuer_sale_xns.aggregate(Sum('xn_shares'))['xn_shares__sum']
        secondary_xns = issuer_sale_xns.exclude(security=prim_sec)
        if secondary_xns.exists():
            for xn in secondary_xns:
                price_date = xn.filedate
                prim_price = \
                    get_price(prim_sph_obj, price_date, issuer, {})
                if prim_price != Decimal(0) and prim_price is not None:
                    prim_share_eqs = xn.xn_val / prim_price
                    number_of_shares_sold += prim_share_eqs
    else:
        number_of_shares_sold = Decimal(0)
    #
    value_of_shares_sold =\
        issuer_sale_xns.aggregate(Sum('xn_val'))['xn_val__sum']
    return number_of_shares_sold, value_of_shares_sold


def replace_company_signals():
    print 'Replacing SignalDisplay objects'
    print '    sorting...'
    a =\
        DiscretionaryXnEvent.objects\
        .values_list('issuer', flat=True).distinct()
    newsignaldisplays = []
    print '    interpreting...'
    counter = 0.0
    looplength = float(len(a))
    for issuer in a:
        # aff_events = DiscretionaryXnEvent.objects.filter(issuer=issuer)
        # When primary ticker concept is added, adjust filter accordingly.

        sec_price_hists = SecurityPriceHist.objects.filter(issuer=issuer)\
            .order_by('security__short_sec_title')
        if sec_price_hists.exists():
            sec_price_hist = sec_price_hists[0]
        else:
            sec_price_hist = None

        person_signals = PersonSignal.objects.filter(issuer=issuer)

        # Buy signal data
        weakness_buys = person_signals\
            .filter(signal_name=buy_response_to_perf).filter(significant=True)
        # Is there only one weakness buy?
        buyonweakness = False
        bow_plural_insiders = None
        bow_start_date = None
        bow_first_sig_detect_date = None
        bow_end_date = None
        bow_person_name = None
        bow_includes_ceo = None
        bow_net_signal_value = None
        bow_first_perf_period_days = None
        bow_first_pre_stock_perf = None
        bow_first_post_stock_perf = None
        if weakness_buys.count() == 1:
            wbuy_signal = weakness_buys[0]
            if is_ceo([wbuy_signal.reporting_person_title]) is True:
                bow_includes_ceo = True
            else:
                bow_includes_ceo = False
            bow_plural_insiders = False
            bow_start_date = wbuy_signal.signal_detect_date
            bow_end_date = wbuy_signal.last_file_date
            bow_first_sig_detect_date = wbuy_signal.first_file_date
            bow_person_name = wbuy_signal.reporting_person.person_name
            bow_net_signal_value = wbuy_signal.net_signal_value
            bow_first_perf_period_days = wbuy_signal.perf_period_days
            bow_first_pre_stock_perf = wbuy_signal.preceding_stock_perf
            bow_first_post_stock_perf = wbuy_signal.perf_after_detection

            buyonweakness = True

        if weakness_buys.count() >= 2:
            bow_start_date = weakness_buys.earliest('first_file_date')\
                .first_file_date
            bow_end_date = weakness_buys.latest('last_file_date')\
                .last_file_date
            first_w_buy = weakness_buys.earliest('signal_detect_date')

            person_titles = \
                weakness_buys.values_list('reporting_person_title', flat=True)
            if is_ceo(person_titles) is True:
                bow_includes_ceo = True
            else:
                bow_includes_ceo = False

            bow_plural_insiders = True
            bow_first_sig_detect_date = first_w_buy.signal_detect_date
            bow_net_signal_value = \
                weakness_buys.aggregate(Sum('net_signal_value'))[
                    'net_signal_value__sum']
            bow_first_perf_period_days = first_w_buy.perf_period_days
            bow_first_pre_stock_perf = first_w_buy.preceding_stock_perf
            bow_first_post_stock_perf = first_w_buy.perf_after_detection

            buyonweakness = True

        # Now address clusterbuy signals, but only if there are not
        # multiple buys on weakness
        clusterbuy = False
        cb_start_date = None
        cb_end_date = None
        cb_plural_insiders = None
        cb_buy_xns = None
        cb_net_xn_value = None
        if weakness_buys.count() <= 1:
            issuer_xns =\
                DiscretionaryXnEvent.objects.filter(issuer=issuer)\
                .filter(filedate__gte=today - signal_detect_lookback)
            buy_xns = issuer_xns.filter(xn_acq_disp_code='A').count()
            net_xn_value =\
                issuer_xns.aggregate(Sum('xn_val'))['xn_val__sum']
            insider_num = len(issuer_xns.filter(xn_acq_disp_code='A')
                              .values_list('reporting_person').distinct())
            if buy_xns >= 3 and net_xn_value >= abs_sig_min:
                if insider_num > 1:
                    cb_plural_insiders = True
                else:
                    cb_plural_insiders = False
                cb_start_date = issuer_xns\
                    .filter(xn_acq_disp_code='A').earliest('filedate')\
                    .filedate
                cb_end_date = issuer_xns\
                    .filter(xn_acq_disp_code='A').latest('filedate')\
                    .filedate
                cb_net_xn_value = net_xn_value
                cb_buy_xns = buy_xns
                clusterbuy = True

        # Now address discretionary buy but only if not obviously precluded
        # by signals that mean the same thing more clearly (i.e. cluster buys,
        # big_discretionarybuys etc).

        discretionarybuy = False
        db_large_xn_size = None
        db_was_ceo = None
        db_start_date = None
        db_detect_date = None
        db_end_date = None
        db_person_name = None
        db_xn_val = None
        db_security_name = None
        db_xn_pct_holdings = None

        if weakness_buys.count() <= 1 and clusterbuy is False:
            person_signals =\
                PersonSignal.objects.filter(issuer=issuer)\
                .filter(signal_name=buy)\
                .filter(significant=True)

            if person_signals.count() > 0:
                person_sig = person_signals.order_by('net_signal_value')[0]
                db_start_date = person_sig.first_file_date
                db_end_date = person_sig.last_file_date
                if person_sig.net_signal_value > big_xn_amt:
                    db_large_xn_size = True
                else:
                    db_large_xn_size = False

                if is_ceo([person_sig.reporting_person_title]) is True:
                    db_was_ceo = True
                else:
                    db_was_ceo = False

                db_detect_date = person_sig.signal_detect_date
                db_person_name = person_sig.reporting_person.person_name
                db_xn_val = person_sig.net_signal_value
                db_security_name = person_sig.security_1.short_sec_title
                db_xn_pct_holdings = person_sig.net_signal_pct

                discretionarybuy = True

        # Sell signal data
        weakness_sells = person_signals\
            .filter(signal_name=sell_response_to_perf).filter(significant=True)
        # Is there only one weakness buy?
        sellonstrength = False
        sos_plural_insiders = None
        sos_start_date = None
        sos_first_sig_detect_date = None
        sos_end_date = None
        sos_person_name = None
        sos_includes_ceo = None
        sos_net_signal_value = None
        sos_first_perf_period_days = None
        sos_first_pre_stock_perf = None
        sos_first_post_stock_perf = None
        if weakness_sells.count() == 1:
            wsell_signal = weakness_sells[0]
            if is_ceo([wsell_signal.reporting_person_title]) is True:
                sos_includes_ceo = True
            else:
                sos_includes_ceo = False
            sos_plural_insiders = False
            sos_start_date = wsell_signal.first_file_date
            sos_end_date = wsell_signal.last_file_date
            sos_first_sig_detect_date = wsell_signal.signal_detect_date
            sos_person_name = wsell_signal.reporting_person.person_name
            sos_net_signal_value = wsell_signal.net_signal_value
            sos_first_perf_period_days = wsell_signal.perf_period_days
            sos_first_pre_stock_perf = wsell_signal.preceding_stock_perf
            sos_first_post_stock_perf = wsell_signal.perf_after_detection

            sellonstrength = True

        if weakness_sells.count() >= 2:
            sos_start_date = weakness_sells.earliest('first_file_date')\
                .first_file_date
            sos_end_date = weakness_sells.latest('last_file_date')\
                .last_file_date
            first_w_sell = weakness_sells.earliest('signal_detect_date')
            person_titles = \
                weakness_sells.values_list('reporting_person_title', flat=True)
            if is_ceo(person_titles) is True:
                sos_includes_ceo = True
            else:
                sos_includes_ceo = False

            sos_plural_insiders = True
            sos_first_sig_detect_date = first_w_sell.signal_detect_date
            sos_net_signal_value = \
                weakness_sells.aggregate(Sum('net_signal_value'))[
                    'net_signal_value__sum']
            sos_first_perf_period_days = first_w_sell.perf_period_days
            sos_first_pre_stock_perf = first_w_sell.preceding_stock_perf
            sos_first_post_stock_perf = first_w_sell.perf_after_detection

            sellonstrength = True

        # Now address clustersell signals, but only if there are not
        # multiple buys on weakness
        clustersell = False
        cs_start_date = None
        cs_end_date = None
        cs_plural_insiders = None
        cs_sell_xns = None
        cs_net_xn_value = None
        cs_net_shares = None
        cs_annual_grant_rate = None
        if weakness_sells.count() <= 1:
            sig_sales =\
                PersonSignal.objects.filter(issuer=issuer)\
                .filter(significant=True)\
                .filter(net_signal_value__lt=Decimal(0))
            net_xn_value =\
                sig_sales.aggregate(Sum('net_signal_value'))[
                    'net_signal_value__sum']
            sell_xns =\
                sig_sales.aggregate(Sum('transactions'))[
                    'transactions__sum']
            net_shares =\
                sig_sales.aggregate(Sum('net_signal_shares'))[
                    'net_signal_shares__sum']
            issuer_xns =\
                DiscretionaryXnEvent.objects.filter(issuer=issuer)\
                .filter(filedate__gte=today - signal_detect_lookback)
            insiders = issuer_xns.filter(xn_acq_disp_code='D')\
                .values_list('reporting_person', flat=True).distinct()
            insider_num = len(insiders)
            annual_grant_rate =\
                Affiliation.objects.filter(reporting_owner__in=insiders)\
                .aggregate(Sum('equity_grant_rate'))[
                    'equity_grant_rate__sum']
            if sell_xns >= 3 and net_xn_value <= -abs_sig_min\
                    and annual_grant_rate is not None\
                    and net_shares <= -annual_grant_rate\
                    and issuer_xns.filter(xn_acq_disp_code='D')\
                    .exclude(filedate=None).exists():
                if insider_num > 1:
                    cs_plural_insiders = True
                else:
                    cs_plural_insiders = False
                cs_start_date = issuer_xns\
                    .filter(xn_acq_disp_code='D').earliest('filedate')\
                    .filedate
                cs_end_date = issuer_xns\
                    .filter(xn_acq_disp_code='D').latest('filedate')\
                    .filedate
                cs_annual_grant_rate = annual_grant_rate
                cs_net_xn_value = net_xn_value
                cs_sell_xns = sell_xns
                cs_net_shares = net_shares

                clustersell = True

        # Now address discretionary buy but only if not obviously precluded
        # by signals that mean the same thing more clearly (i.e. cluster buys,
        # big_discretionarybuys etc).

        discretionarysell = False
        ds_large_xn_size = None
        ds_was_ceo = None
        ds_start_date = None
        ds_end_date = None
        ds_detect_date = None
        ds_person_name = None
        ds_xn_val = None
        ds_security_name = None
        ds_xn_pct_holdings = None

        if weakness_sells.count() <= 1 and clustersell is False:
            person_signals =\
                PersonSignal.objects.filter(issuer=issuer)\
                .filter(signal_name=sell)\
                .filter(significant=True)

            if person_signals.count() > 0:
                person_sig = person_signals.order_by('net_signal_value')[0]
                if person_sig.net_signal_value < -big_xn_amt:
                    ds_large_xn_size = True
                else:
                    ds_large_xn_size = False

                if is_ceo([person_sig.reporting_person_title]) is True:
                    ds_was_ceo = True
                else:
                    ds_was_ceo = False
                ds_start_date = person_sig.first_file_date
                ds_end_date = person_sig.last_file_date
                ds_detect_date = person_sig.signal_detect_date
                ds_person_name = person_sig.reporting_person.person_name
                ds_xn_val = person_sig.net_signal_value
                ds_security_name = person_sig.security_1.short_sec_title
                ds_xn_pct_holdings = person_sig.net_signal_pct

                discretionarysell = True

        signal_dates = []
        signal_dates = appendif(signal_dates, bow_first_sig_detect_date)
        signal_dates = appendif(signal_dates, cb_end_date)
        signal_dates = appendif(signal_dates, db_detect_date)

        signal_dates = appendif(signal_dates, sos_first_sig_detect_date)
        signal_dates = appendif(signal_dates, cs_end_date)
        signal_dates = appendif(signal_dates, ds_detect_date)
        last_signal = None
        if len(signal_dates) != 0:
            last_signal = max(signal_dates)
        if last_signal == date_of_any_new_filings:
            signal_is_new = True
        else:
            signal_is_new = False
        total_transactions = DiscretionaryXnEvent.objects\
            .filter(filedate__gte=today - signal_detect_lookback)\
            .filter(issuer=issuer).count()
        issuer_affiliations = Affiliation.objects.filter(issuer=issuer)
        active_insiders = issuer_affiliations.filter(is_active=True).count()
        sellers = issuer_affiliations.filter(behavior=seller).count()
        holders_with_lower_holdings = issuer_affiliations\
            .filter(prior_share_equivalents_held__gt=F(
                'share_equivalents_held'))\
            .values_list('prior_share_equivalents_held',
                         'share_equivalents_held')
        if len(holders_with_lower_holdings) > 0:
            total_share_holding_drop = Decimal(0)
            for prior, current in holders_with_lower_holdings:
                total_share_holding_drop = prior - current
            insiders_reduced_holdings = len(holders_with_lower_holdings)
            average_holding_reduction = \
                total_share_holding_drop / Decimal(insiders_reduced_holdings)
        else:
            insiders_reduced_holdings = 0
            average_holding_reduction = None
        # Assign recent selling and historical selling numbers
        number_of_recent_shares_sold, value_of_recent_shares_sold =\
            agg_selling_activity(issuer, today - recent_sale_period, today)
        historical_shares_sold, value_of_hist_shares_sold =\
            agg_selling_activity(issuer, today - hist_sale_period,
                                 today - recent_sale_period)
        historical_selling_rate_shares =\
            historical_shares_sold * Decimal(recent_sale_period.days) /\
            Decimal(hist_sale_period.days)

        historical_selling_rate_value =\
            value_of_hist_shares_sold * Decimal(recent_sale_period.days) /\
            Decimal(hist_sale_period.days)

        # percent_change_in_shares_historical_to_recent

        # percent_change_in_value_historical_to_recent

        # percent_options_converted_to_expire_in_current_year

        # percent_recent_shares_sold_under_10b5_1_plans

        # recent_share_sell_rate_for_10b5_1_plans

        # historical_share_sell_rate_for_10b5_1_plans

        sigtoappend =\
            SigDisplay(
                issuer_id=issuer,
                sec_price_hist=sec_price_hist,
                last_signal=last_signal,
                buyonweakness=buyonweakness,
                bow_plural_insiders=bow_plural_insiders,
                bow_start_date=bow_start_date,
                bow_end_date=bow_end_date,
                bow_first_sig_detect_date=bow_first_sig_detect_date,
                bow_person_name=bow_person_name,
                bow_includes_ceo=bow_includes_ceo,
                bow_net_signal_value=bow_net_signal_value,
                bow_first_perf_period_days=bow_first_perf_period_days,
                bow_first_pre_stock_perf=bow_first_pre_stock_perf,
                bow_first_post_stock_perf=bow_first_post_stock_perf,
                clusterbuy=clusterbuy,
                cb_start_date=cb_start_date,
                cb_end_date=cb_end_date,
                cb_plural_insiders=cb_plural_insiders,
                cb_buy_xns=cb_buy_xns,
                cb_net_xn_value=cb_net_xn_value,
                discretionarybuy=discretionarybuy,
                db_large_xn_size=db_large_xn_size,
                db_was_ceo=db_was_ceo,
                db_start_date=db_start_date,
                db_end_date=db_end_date,
                db_detect_date=db_detect_date,
                db_person_name=db_person_name,
                db_xn_val=db_xn_val,
                db_security_name=db_security_name,
                db_xn_pct_holdings=db_xn_pct_holdings,
                sellonstrength=sellonstrength,
                sos_plural_insiders=sos_plural_insiders,
                sos_start_date=sos_start_date,
                sos_end_date=sos_end_date,
                sos_first_sig_detect_date=sos_first_sig_detect_date,
                sos_person_name=sos_person_name,
                sos_includes_ceo=sos_includes_ceo,
                sos_net_signal_value=sos_net_signal_value,
                sos_first_perf_period_days=sos_first_perf_period_days,
                sos_first_pre_stock_perf=sos_first_pre_stock_perf,
                sos_first_post_stock_perf=sos_first_post_stock_perf,
                clustersell=clustersell,
                cs_start_date=cs_start_date,
                cs_end_date=cs_end_date,
                cs_plural_insiders=cs_plural_insiders,
                cs_sell_xns=cs_sell_xns,
                cs_net_xn_value=cs_net_xn_value,
                cs_net_shares=cs_net_shares,
                cs_annual_grant_rate=cs_annual_grant_rate,
                discretionarysell=discretionarysell,
                ds_large_xn_size=ds_large_xn_size,
                ds_was_ceo=ds_was_ceo,
                ds_start_date=ds_start_date,
                ds_end_date=ds_end_date,
                ds_detect_date=ds_detect_date,
                ds_person_name=ds_person_name,
                ds_xn_val=ds_xn_val,
                ds_security_name=ds_security_name,
                ds_xn_pct_holdings=ds_xn_pct_holdings,
                total_transactions=total_transactions,
                active_insiders=active_insiders,
                sellers=sellers,
                insiders_reduced_holdings=insiders_reduced_holdings,
                average_holding_reduction=average_holding_reduction,
                number_of_recent_shares_sold=number_of_recent_shares_sold,
                value_of_recent_shares_sold=value_of_recent_shares_sold,
                historical_selling_rate_shares=historical_selling_rate_shares,
                historical_selling_rate_value=historical_selling_rate_value,
                # mixed_signals=mixed_signals,
                signal_is_new=signal_is_new)

        if buyonweakness is not None\
                or clusterbuy is not None\
                or discretionarybuy is not None\
                or sellonstrength is not None\
                or clustersell is not None\
                or discretionarysell is not None:
            newsignaldisplays.append(sigtoappend)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s company signal views to analyze: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\n    %s objects to save...' % len(newsignaldisplays)
    print '    deleting old and saving...'
    SigDisplay.objects.all().delete()
    SigDisplay.objects.bulk_create(newsignaldisplays)
    print 'done.'
    django.db.reset_queries()
    print ''
    return


def updatewatchednames():
    'Updating WatchedName last signal dates...'
    '   finding entries to update...'
    new_sigs = \
        SigDisplay.objects.filter(signal_is_new=True)
    '   updating...'
    for sig in new_sigs:
        issuer = sig.issuer
        sig_watchnames = WatchedName.objects.filter(issuer=issuer)
        if sig_watchnames.exists():
            sig_watchnames.update(last_signal_sent=sig.last_signal)
    '   done.'
    return

print 'Populating signals...'
create_disc_xn_events()
replace_person_signals()
replace_company_signals()
updatewatchednames()
