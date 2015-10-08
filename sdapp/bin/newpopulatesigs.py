import datetime
# import pytz
from decimal import Decimal

import django.db
from django.db.models import F, Q, Sum

from sdapp.models import DiscretionaryXnEvent, Form345Entry, PersonSignal,\
    SecurityPriceHist, ClosePrice
# from sdapp.models import WatchedName
from sdapp.bin.globals import signal_detect_lookback, significant_stock_move,\
    abs_sig_min, rel_sig_min, perf_period_days, today, todaymid,\
    buy, buy_response_to_perf, sell, sell_response_to_perf, big_xn_amt


def calc_holdings(securities, issuer, reporting_person):
    first_filing_date = securities[0][3]
    ticker_security =\
        SecurityPriceHist.objects.filter(issuer=issuer)[0].security
    person_forms =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(reporting_owner_cik=reporting_person)\
        .exclude(supersededdt__lt=first_filing_date - datetime.timedelta(1))\
        .exclude(filedatetime__gte=first_filing_date - datetime.timedelta(1))
    stock_values = person_forms\
        .filter(security=ticker_security)\
        .exclude(reported_shares_following_xn=None)\
        .values_list('reported_shares_following_xn', 'adjustment_factor')
    stock_deriv_values = person_forms\
        .filter(underlying_security=ticker_security)\
        .exclude(underlying_shares=None)\
        .values_list('underlying_shares', 'adjustment_factor')
    all_values = list(stock_values) + list(stock_deriv_values)
    prior_holding_value = Decimal(0)
    for rep_shares, adj_factor in all_values:
        prior_holding_value += Decimal(rep_shares) * Decimal(adj_factor)

    return prior_holding_value


def laxer_start_price(sec_price_hist, date):
    wkd_td = datetime.timedelta(5)
    close_prices = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)
    price_list = \
        close_prices.filter(close_date__lte=date-wkd_td)\
        .filter(close_date__gte=date).order_by('close_date')
    if price_list.exists():
        return price_list[0].adj_close_price
    else:
        return None


def get_price(sec_price_hist, date):
    close_price = \
        ClosePrice.objects.filter(securitypricehist=sec_price_hist)\
        .filter(close_date=date)
    if close_price.exists():
        return close_price[0].adj_close_price
    else:
        return laxer_start_price(sec_price_hist, date)


def calc_perf(later_price, earlier_price):
    stock_perf = None
    if later_price is not None\
            and earlier_price is not None:
        stock_perf =\
            round((later_price /
                   earlier_price)
                  - Decimal(1), 4)
    return stock_perf


def is_ceo(person_xn_list):
    keywords = ['ceo', 'chief executive officer',
                'principal exeuctive officer']
    ceo_match = False
    for person_xn in person_xn_list:
        lowercase_title = person_xn.reporting_person_title.lower()
        for keyword in keywords:
            if lowercase_title in keyword:
                ceo_match = True
    return ceo_match


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


def calc_grants(issuer_cik, reporting_person_cik):
    grants = Form345Entry.objects.filter(issuer_cik=issuer_cik)\
        .filter(reporting_owner_cik=reporting_person_cik)\
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
        grant_shares_adjusted += xn_shares * adj_factor * conv_mult
    # Annualize latest grant
    eq_annual_share_grants = grant_shares_adjusted * grants_per_year

    return eq_annual_share_grants


def create_disc_xn_events():

    print 'Creating new discretionary transaction objects'
    print '    sorting...'

    existing_sig_pks =\
        DiscretionaryXnEvent.objects.values_list('form_entry__pk')

    # Note that the below contains an 'F Object'; since this may be unfamiliar,
    # I will explain -- it filters for transaction dates that are greater than
    # 5 days (timedelta) before the filedatetime.  This avoids interpreting an
    # old transaction in a newly filed form as a new signal.

    a =\
        Form345Entry.objects\
        .filter(filedatetime__gte=todaymid + signal_detect_lookback)\
        .filter(transaction_date__gte=F('filedatetime')
                + datetime.timedelta(-5))\
        .exclude(transaction_date=None)\
        .exclude(xn_price_per_share=None)\
        .exclude(transaction_shares=None)\
        .exclude(xn_acq_disp_code=None)\
        .filter(Q(transaction_code='P') | Q(transaction_code='S'))\
        .exclude(pk__in=existing_sig_pks)
    newxns = []
    print '    interpreting...'
    for item in a:
        if item.xn_acq_disp_code == 'D':
            sign_transaction_shares = \
                Decimal(-1) * item.transaction_shares * item.adjustment_factor
            xn_val = Decimal(-1) * item.xn_price_per_share
        else:
            sign_transaction_shares = \
                item.transaction_shares * item.adjustment_factor
            xn_val = item.xn_price_per_share
        newxn =\
            DiscretionaryXnEvent(issuer=item.issuer_cik,
                                 reporting_person=item.reporting_owner_cik,
                                 security=item.security,
                                 form_entry=item.pk,
                                 xn_acq_disp_code=item.xn_acq_disp_code,
                                 transaction_code=item.transaction_code,
                                 xn_val=xn_val,
                                 xn_shares=sign_transaction_shares,
                                 filedate=item.filedatetime.date)
        newxns.append(newxn)
    print '    saving...'
    DiscretionaryXnEvent.objects.bulk_create(newxns)

    print 'done.'
    django.db.reset_queries()
    print ''
    return


def replace_person_signals():
    print 'Replacing PersonSignal objects'
    print '    sorting...'
    a =\
        DiscretionaryXnEvent.objects\
        .values_list('reporting_person', 'issuer').distinct()
    newpersonsignals = []
    print '    interpreting...'
    for reporting_person, issuer in a:
        # When primary ticker concept is added, adjust filter accordingly.
        aff_events = DiscretionaryXnEvent.objects.filter(issuer=issuer)\
            .filter(reporting_person=reporting_person)
        sec_price_hist = SecurityPriceHist.objects.filter(issuer=issuer)\
            .order_by('security__short_sec_title')[0]
        reporting_person_title = \
            Form345Entry.objects.filter(reporting_owner_cik=reporting_person)\
            .filter(filedatetime__gte=todaymid + signal_detect_lookback)\
            .latest('filedatetime').person_title

        securities = aff_events.order_by('filedate')\
            .values_list('security', 'xn_val', 'xn_shares', 'filedate')

        entryfiledates = aff_events.order_by('filedate')\
            .order_by('filedatetime').values_list('filedatetime', flat=True)
        first_file_date = entryfiledates[0].date()
        last_file_date = entryfiledates[-1].date()
        transactions = len(entryfiledates)

        eq_annual_share_grants = calc_grants(issuer, reporting_person)

        # Get holdings before form filed
        prior_holding_value =\
            calc_holdings(securities, issuer, reporting_person)
        securities_dict = {}
        net_signal_value = Decimal(0)
        gross_acq_value = Decimal(0)
        gross_disp_value = Decimal(0)

# CONSIDIER REMOVING SECURITY_1 CONCEPT FROM PERSON SIGNALS
# SET UP SIGNIFICANCE AND SIGNAL DETECT DATE BASED ON NET XNS FOR EACH DATE
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

            net_signal_value += xn_val

            if xn_val > 0:
                gross_acq_value += xn_val
            else:
                gross_disp_value += xn_val

        signal_detect_date = None
        net_val_of_date = Decimal(0)
        net_shares_of_date = Decimal(0)
        # Find the date activity became significant.
        for filedate, [net_xn_value, net_xn_shares] in\
                sorted(filedate_dict.iteritems()):
            net_val_of_date += net_xn_value
            net_shares_of_date += net_xn_shares
            # This tests if the transactions to date are significant
            # and if so and if the signal was not yet detected, it sets the
            # date of detection.
            if net_signal_value > Decimal(0):
                if prior_holding_value > Decimal(0)\
                        and net_val_of_date >= abs_sig_min\
                        and net_val_of_date / prior_holding_value >=\
                        rel_sig_min\
                        and net_shares_of_date > eq_annual_share_grants\
                        and signal_detect_date is not None:
                    signal_detect_date = filedate
                    significant = True
            else:
                if prior_holding_value > Decimal(0)\
                        and net_val_of_date <= -abs_sig_min\
                        and net_val_of_date / prior_holding_value <=\
                        -rel_sig_min\
                        and -net_shares_of_date > eq_annual_share_grants\
                        and signal_detect_date is not None:
                    signal_detect_date = filedate
                    significant = True






        # This fills in the last transaction date if signal is not significant.
        if signal_detect_date is None:
            signal_detect_date = last_file_date
        stock_price_for_perf_lookback =\
            get_price(sec_price_hist, filedate + perf_period_days)
        stock_price_at_detection = get_price(sec_price_hist, filedate)
        stock_price_now = get_price(sec_price_hist, filedate)

        preceding_stock_perf =\
            calc_perf(stock_price_at_detection, stock_price_for_perf_lookback)
        perf_after_detection =\
            calc_perf(stock_price_now, stock_price_at_detection)
        subs_stock_period_days = (todaymid.date() - signal_detect_date).days

        # This determines the gross signal value whether a net buy or sale
        if gross_acq_value >= Decimal(-1) * gross_disp_value:
            gross_signal_value = gross_acq_value
        else:
            gross_signal_value = gross_disp_value
        # This assigns the signal anme
        if gross_acq_value >= 0:
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

        security_1 = max(securities_dict, key=securities_dict.get)
        average_price_security_1 =\
            securities_dict[security_1][0] / securities_dict[security_1][1]
        net_signal_pct = net_signal_value / gross_signal_value * Decimal(100)
        if len(securities_dict) == 1:
            only_security_1 = True
        else:
            only_security_1 = False

        newpersonsignals.append(
            PersonSignal(issuer=issuer,
                         sec_price_hist=sec_price_hist,
                         reporting_person=reporting_person,
                         eq_annual_share_grants=eq_annual_share_grants,
                         security_1=security_1,
                         only_security_1=only_security_1,
                         reporting_person_title=reporting_person_title,
                         signal_name=signal_name,
                         signal_detect_date=signal_detect_date,
                         first_file_date=first_file_date,
                         last_file_date=last_file_date,
                         transactions=transactions,
                         average_price_security_1=average_price_security_1,
                         gross_signal_value=gross_signal_value,
                         net_signal_value=net_signal_value,
                         prior_holding_value=prior_holding_value,
                         net_signal_pct=net_signal_pct,
                         preceding_stock_perf=preceding_stock_perf,
                         perf_period_days=perf_period_days,
                         perf_after_detection=perf_after_detection,
                         subs_stock_period_days=subs_stock_period_days,
                         significant=significant,
                         new=True))
    print '    deleting old and saving...'
    PersonSignal.objects.all().delete()
    PersonSignal.objects.bulk_create(newpersonsignals)
    print 'done.'
    django.db.reset_queries()
    print ''
    return


def replace_company_signals():
    print 'Replacing SignalDisplay objects'
    print '    sorting...'
    a =\
        DiscretionaryXnEvent.objects\
        .values_list('issuer').distinct()
    newsignaldisplays = []
    print '    interpreting...'
    for issuer in a:
        # aff_events = DiscretionaryXnEvent.objects.filter(issuer=issuer)
        # When primary ticker concept is added, adjust filter accordingly.
        sec_price_hist = SecurityPriceHist.objects.filter(issuer=issuer)\
            .order_by('security__short_sec_title')[0]
        person_signals = PersonSignal.objects.filter(issuer=issuer)


        weakness_sells = person_signals\
            .filter(signal_name=sell_response_to_perf).filter(significant=True)
        # Is there only one weakness buy?
        sow_plural_insiders = None
        sow_first_sig_detect_date = None
        sow_person_name = None
        sow_includes_ceo = None
        sow_net_signal_value = None
        sow_first_perf_period_days = None
        sow_first_pre_stock_perf = None
        sow_first_post_stock_perf = None
        if weakness_sells.count() == 1:
            wsell_signal = weakness_sells[0]
            if is_ceo([wsell_signal.reporting_person_title]) is True:
                ceo_note = "the CEO, "
                sow_includes_ceo = True
            else:
                ceo_note = ""
                sow_includes_ceo = False
            sow_plural_insiders = False
            sow_first_sig_detect_date = wsell_signal.signal_detect_date
            sow_person_name = wsell_signal.reporting_person.person_name
            sow_net_signal_value = wsell_signal.net_signal_value
            sow_first_perf_period_days = wsell_signal.perf_period_days
            sow_first_pre_stock_perf = wsell_signal.preceding_stock_perf
            sow_first_post_stock_perf = wsell_signal.perf_after_detection

            sub_tuple = (sow_first_sig_detect_date,
                         sow_person_name,
                         ceo_note,
                         -sow_net_signal_value,
                         sow_first_perf_period_days,
                         sow_first_pre_stock_perf,
                         sow_first_post_stock_perf)

            sell_on_weakness =\
                "%s - %s %ssold $%s of company securities "\
                "when %s day stock performance was %s%%. Since then the "\
                "stock has returned %s." \
                % sub_tuple

        if weakness_sells.count() >= 2:
            first_w_sell = weakness_sells.latest('signal_detect_date')
            person_titles = \
                weakness_sells.values_list('reporting_person_title', flat=True)
            if is_ceo(person_titles) is True:
                ceo_note = "including by CEO, "
                sow_includes_ceo = True
            else:
                ceo_note = ""
                sow_includes_ceo = False

            sow_plural_insiders = True
            sow_first_sig_detect_date = first_w_sell.signal_detect_date
            sow_net_signal_value = \
                weakness_sells.aggregate(Sum('net_signal_value'))
            sow_first_perf_period_days = first_w_sell.perf_period_days
            sow_first_pre_stock_perf = first_w_sell.preceding_stock_perf
            sow_first_post_stock_perf = first_w_sell.perf_after_detection

            sub_tuple = (sow_first_sig_detect_date,
                         ceo_note,
                         -sow_net_signal_value,
                         sow_first_perf_period_days,
                         sow_first_pre_stock_perf,
                         sow_first_post_stock_perf)

            sell_on_weakness =\
                "%s - Insider selling activity %sof $%s of company "\
                "securities initially detected after %s day stock "\
                "performance of %s%%. Since then the stock "\
                "has returned %s." \
                % sub_tuple
        # Now address cluster_sell signals, but only if there are not
        # multiple buys on weakness
        cluster_sell = None
        cs_plural_insiders = None
        cs_sell_xns = None
        cs_net_xn_value = None
        if weakness_sells.count() <= 1:
            issuer_xns =\
                DiscretionaryXnEvent.objects.filter(issuer=issuer)

            cs_sell_xns = issuer_xns.filter(xn_acq_disp_code='A').count()
            cs_net_xn_value = issuer_xns.aggregate(Sum('xn_val'))
            insider_num = len(issuer_xns.filter(xn_acq_disp_code='A')
                              .values_list('reporting_person').distinct())
            if insider_num > 1:
                plural_insiders = 's'
                cs_plural_insiders = True
            else:
                plural_insiders = ''
                cs_plural_insiders = False
            if cs_sell_xns >= 3 and cs_net_xn_value <= -abs_sig_min:
                sub_tuple = (plural_insiders, cs_sell_xns, -cs_net_xn_value)
                cluster_sell =\
                    "Recent net selling activity by insider%s"\
                    "was $%s over %s transactions."\
                    % sub_tuple

        # Now address discretionary buy but only if not obviously precluded
        # by signals that mean the same thing more clearly (i.e. cluster buys,
        # big_discretionary_buys etc).

        discretionary_sell = None
        ds_large_xn_size = None
        ds_was_ceo = None
        ds_detect_date = None
        ds_person_name = None
        ds_xn_val = None
        ds_security_name = None
        ds_xn_pct_holdings = None

        if weakness_sells.count() <= 1 and cluster_sell is None:
            person_signals =\
                PersonSignal.objects.filter(issuer=issuer)\
                .filter(signal_name=buy)\
                .filter(significant=True)

            if person_signals.count() > 0:
                person_xn = person_signals.order_by('net_signal_value')[0]
                if person_xn.net_signal_value < -big_xn_amt:
                    xn_size_note = "In a large transaction on"
                    ds_large_xn_size = True
                else:
                    xn_size_note = "On"
                    ds_large_xn_size = False

                if is_ceo([person_xn]) is True:
                    ceo_note = ", the CEO,"
                    ds_was_ceo = True
                else:
                    ceo_note = ""
                    ds_was_ceo = False

                ds_detect_date = person_xn.signal_detect_date
                ds_person_name = person_xn.reporting_person.person_name
                ds_xn_val = person_xn.net_signal_value
                ds_security_name = person_xn.security.short_sec_title
                ds_xn_pct_holdings = person_xn.net_signal_pct

                sub_tuple = (xn_size_note, ds_detect_date, ds_person_name,
                             ceo_note, -ds_xn_val, ds_security_name,
                             ds_xn_pct_holdings)

                discretionary_sell =\
                    "%s %s, %s%s sold $%s of %s (%s%% of total holdings)."











        weakness_buys = person_signals\
            .filter(signal_name=buy_response_to_perf).filter(significant=True)
        # Is there only one weakness buy?
        bow_plural_insiders = None
        bow_first_sig_detect_date = None
        bow_person_name = None
        bow_includes_ceo = None
        bow_net_signal_value = None
        bow_first_perf_period_days = None
        bow_first_pre_stock_perf = None
        bow_first_post_stock_perf = None
        if weakness_buys.count() == 1:
            wbuy_signal = weakness_buys[0]
            if is_ceo([wbuy_signal.reporting_person_title]) is True:
                ceo_note = "the CEO, "
                bow_includes_ceo = True
            else:
                ceo_note = ""
                bow_includes_ceo = False
            bow_plural_insiders = False
            bow_first_sig_detect_date = wbuy_signal.signal_detect_date
            bow_person_name = wbuy_signal.reporting_person.person_name
            bow_net_signal_value = wbuy_signal.net_signal_value
            bow_first_perf_period_days = wbuy_signal.perf_period_days
            bow_first_pre_stock_perf = wbuy_signal.preceding_stock_perf
            bow_first_post_stock_perf = wbuy_signal.perf_after_detection

            sub_tuple = (bow_first_sig_detect_date,
                         bow_person_name,
                         ceo_note,
                         bow_net_signal_value,
                         bow_first_perf_period_days,
                         bow_first_pre_stock_perf,
                         bow_first_post_stock_perf)

            buy_on_weakness =\
                "%s - %s %sacquired $%s of company securities "\
                "when %s day stock performance was %s%%. Since then the "\
                "stock has returned %s." \
                % sub_tuple

        if weakness_buys.count() >= 2:
            first_w_buy = weakness_buys.latest('signal_detect_date')
            person_titles = \
                weakness_buys.values_list('reporting_person_title', flat=True)
            if is_ceo(person_titles) is True:
                ceo_note = "including by CEO, "
                bow_includes_ceo = True
            else:
                ceo_note = ""
                bow_includes_ceo = False

            bow_plural_insiders = True
            bow_first_sig_detect_date = first_w_buy.signal_detect_date
            bow_net_signal_value = \
                weakness_buys.aggregate(Sum('net_signal_value'))
            bow_first_perf_period_days = first_w_buy.perf_period_days
            bow_first_pre_stock_perf = first_w_buy.preceding_stock_perf
            bow_first_post_stock_perf = first_w_buy.perf_after_detection

            sub_tuple = (bow_first_sig_detect_date,
                         ceo_note,
                         bow_net_signal_value,
                         bow_first_perf_period_days,
                         bow_first_pre_stock_perf,
                         bow_first_post_stock_perf)

            buy_on_weakness =\
                "%s - Insider buying activity %sof $%s of company "\
                "securities initially detected after %s day stock "\
                "performance of %s%%. Since then the stock "\
                "has returned %s." \
                % sub_tuple
        # Now address cluster_buy signals, but only if there are not
        # multiple buys on weakness
        cluster_buy = None
        cb_plural_insiders = None
        cb_buy_xns = None
        cb_net_xn_value = None
        if weakness_buys.count() <= 1:
            issuer_xns =\
                DiscretionaryXnEvent.objects.filter(issuer=issuer)

            cb_buy_xns = issuer_xns.filter(xn_acq_disp_code='A').count()
            cb_net_xn_value = issuer_xns.aggregate(Sum('xn_val'))
            insider_num = len(issuer_xns.filter(xn_acq_disp_code='A')
                              .values_list('reporting_person').distinct())
            if insider_num > 1:
                plural_insiders = 's'
                cb_plural_insiders = True
            else:
                plural_insiders = ''
                cb_plural_insiders = False
            if cb_buy_xns >= 3 and cb_net_xn_value >= abs_sig_min:
                sub_tuple = (plural_insiders, cb_buy_xns, cb_net_xn_value)
                cluster_buy =\
                    "Recent net buying activity by insider%s"\
                    "was $%s over %s transactions."\
                    % sub_tuple

        # Now address discretionary buy but only if not obviously precluded
        # by signals that mean the same thing more clearly (i.e. cluster buys,
        # big_discretionary_buys etc).

        discretionary_buy = None
        db_large_xn_size = None
        db_was_ceo = None
        db_detect_date = None
        db_person_name = None
        db_xn_val = None
        db_security_name = None
        db_xn_pct_holdings = None

        if weakness_buys.count() <= 1 and cluster_buy is None:
            person_signals =\
                PersonSignal.objects.filter(issuer=issuer)\
                .filter(signal_name=buy)\
                .filter(significant=True)

            if person_signals.count() > 0:
                person_xn = person_signals.order_by('net_signal_value')[0]
                if person_xn.net_signal_value > big_xn_amt:
                    xn_size_note = "In a large transaction on"
                    db_large_xn_size = True
                else:
                    xn_size_note = "On"
                    db_large_xn_size = False

                if is_ceo([person_xn]) is True:
                    ceo_note = ", the CEO,"
                    db_was_ceo = True
                else:
                    ceo_note = ""
                    db_was_ceo = False

                db_detect_date = person_xn.signal_detect_date
                db_person_name = person_xn.reporting_person.person_name
                db_xn_val = person_xn.net_signal_value
                db_security_name = person_xn.security.short_sec_title
                db_xn_pct_holdings = person_xn.net_signal_pct

                sub_tuple = (xn_size_note, db_detect_date, db_person_name,
                             ceo_note, db_xn_val, db_security_name,
                             db_xn_pct_holdings)

                discretionary_buy =\
                    "%s %s, %s%s bought $%s of %s (%s%% of total holdings)."










        total_transactions = DiscretionaryXnEvent.objects\
            .filter(issuer=issuer).count()

        newsignaldisplays.append(
            PersonSignal(issuer=issuer,
                         sec_price_hist=sec_price_hist,
                         buy_on_weakness=buy_on_weakness,
                         bow_plural_insiders=bow_plural_insiders,
                         bow_first_sig_detect_date=bow_first_sig_detect_date,
                         bow_person_name=bow_person_name,
                         bow_includes_ceo=bow_includes_ceo,
                         bow_net_signal_value=bow_net_signal_value,
                         bow_first_perf_period_days=bow_first_perf_period_days,
                         bow_first_pre_stock_perf=bow_first_pre_stock_perf,
                         bow_first_post_stock_perf=bow_first_post_stock_perf,
                         cluster_buy=cluster_buy,
                         cb_plural_insiders=cb_plural_insiders,
                         cb_buy_xns=cb_buy_xns,
                         cb_net_xn_value=cb_net_xn_value,
                         discretionary_buy=discretionary_buy,
                         db_large_xn_size=db_large_xn_size,
                         db_was_ceo=db_was_ceo,
                         db_detect_date=db_detect_date,
                         db_person_name=db_person_name,
                         db_xn_val=db_xn_val,
                         db_security_name=db_security_name,
                         db_xn_pct_holdings=db_xn_pct_holdings,
                         # 
                         sell_on_weakness=sell_on_weakness,
                         sow_plural_insiders=sow_plural_insiders,
                         sow_first_sig_detect_date=sow_first_sig_detect_date,
                         sow_person_name=sow_person_name,
                         sow_includes_ceo=sow_includes_ceo,
                         sow_net_signal_value=sow_net_signal_value,
                         sow_first_perf_period_days=sow_first_perf_period_days,
                         sow_first_pre_stock_perf=sow_first_pre_stock_perf,
                         sow_first_post_stock_perf=sow_first_post_stock_perf,
                         cluster_sell=cluster_sell,
                         cs_plural_insiders=cs_plural_insiders,
                         cs_sell_xns=cs_sell_xns,
                         cs_net_xn_value=cs_net_xn_value,
                         discretionary_sell=discretionary_sell,
                         ds_large_xn_size=ds_large_xn_size,
                         ds_was_ceo=ds_was_ceo,
                         ds_detect_date=ds_detect_date,
                         ds_person_name=ds_person_name,
                         ds_xn_val=ds_xn_val,
                         ds_security_name=ds_security_name,
                         ds_xn_pct_holdings=ds_xn_pct_holdings,
                         # sell_on_strength=sell_on_strength,
                         # cluster_sell=cluster_sell,
                         # big_discretionary_sell=big_discretionary_sell,
                         # ceo_sell=ceo_sell,
                         # discretionary_sells=discretionary_sell,
                         total_transactions=total_transactions,
                         # mixed_signals=mixed_signals,
                         signal_is_new=True))

    print '    deleting old and saving...'
    PersonSignal.objects.all().delete()
    PersonSignal.objects.bulk_create(newsignaldisplays)
    print 'done.'
    django.db.reset_queries()
    print ''
    return


print 'Populating signals...'
create_disc_xn_events()
replace_person_signals()
replace_company_signals()
positive_sig = True