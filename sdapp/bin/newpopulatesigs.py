import datetime
# import pytz
from decimal import Decimal

import django.db
from django.db.models import F, Q

from sdapp.models import DiscretionaryXnEvent, Form345Entry, PersonSignal,\
    SecurityPriceHist, ClosePrice
# from sdapp.models import WatchedName
from sdapp.bin.globals import signal_detect_lookback, significant_stock_move,\
    abs_holding_min, rel_holding_min, perf_period_days, todaymid,\
    buy, buy_response_to_perf, sell, sell_response_to_perf


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
            sign_transaction_shares = Decimal(-1) * item.transaction_shares
        else:
            sign_transaction_shares = item.transaction_shares
        xn_val = item.xn_price_per_share * sign_transaction_shares
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

        # Get holdings before form filed
        prior_holding_value =\
            calc_holdings(securities, issuer, reporting_person)
        securities_dict = {}
        net_signal_value = Decimal(0)
        gross_acq_value = Decimal(0)
        gross_disp_value = Decimal(0)
        signal_detect_date = None
        significant = False
        for security, xn_val, xn_shares, filedate in securities:
            # Is the transaction security in the tracking dict object?
            # If so, add to existing key; if not, add a dict key for it.
            if security in securities_dict:
                securities_dict[security][0] += xn_val
                securities_dict[security][1] += xn_shares
            else:
                securities_dict[security] = [xn_val, xn_shares]
            net_signal_value += xn_val
            # This tests first if the transaction to day are significant
            # and if so and if the signal was not yet detected, it sets the
            # date of detection.
            #
            # The "else" below functions to take away a signal_detect_date
            # if the signal was is rendered insiginificant by the holder
            # selling part of what the holder previously bought.
            if prior_holding_value > Decimal(0)\
                    and net_signal_value >= abs_holding_min\
                    and net_signal_value / prior_holding_value >=\
                    rel_holding_min:
                if signal_detect_date is None:
                    signal_detect_date = filedate
                    significant = True
            else:
                signal_detect_date = None
                significant = False

            if xn_val > 0:
                gross_acq_value += xn_val
            else:
                gross_disp_value += xn_val
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

        weakness_buys = person_signals.filter(signal_name=buy_response_to_perf)
        # Is there only one weakness buy?
        if weakness_buys.count() == 1:
            wbuy_signal = weakness_buys[0]
            if issuer.current_ceo == wbuy_signal.reporting_person:
                ceo_note = "the CEO, "
            else:
                ceo_note = ""
            sub_tuple = (wbuy_signal.signal_detect_date,
                         wbuy_signal.reporting_person.person_name,
                         ceo_note,
                         wbuy_signal.net_signal_value,
                         wbuy_signal.perf_period_days,
                         wbuy_signal.preceding_stock_perf,
                         wbuy_signal.perf_after_detection)

            buy_on_weakness =\
                "%s - %s %sacquired $%s of company securities "\
                "when %s day stock performance was %s%%. Since then the "\
                "stock has returned %s." \
                % sub_tuple

        if weakness_buys.count() >= 2:
            first_w_buy = weakness_buys.latest('signal_detect_date')
            earliest_detect_date = first_w_buy.signal_detect_date
            earliest_preceding_perf = first_w_buy.preceding_stock_perf
            earliest_subs_perf = first_w_buy.perf_after_detection
            person_ciks = \
                weakness_buys.values_list('reporting_person', flat=True)
            if issuer.current_ceo in person_ciks:
                ceo_note = "including by CEO, "
            else:
                ceo_note = ""

            sub_tuple = (earliest_detect_date,
                         ceo_note,
                         wbuy_signal.net_signal_value,
                         wbuy_signal.perf_period_days,
                         earliest_preceding_perf,
                         earliest_subs_perf)

            buy_on_weakness =\
                "%s - Insider buying activity %sof $%s of company "\
                "securities initially detected after %s day stock "\
                "performance of %s%%. Since then the stock "\
                "has returned %s." \
                % sub_tuple


        newsignaldisplays.append(
            PersonSignal(issuer=issuer,
                         sec_price_hist=sec_price_hist,
                         buy_on_weakness=buy_on_weakness,
                         cluster_buy=cluster_buy,
                         discretionary_buy=discretionary_buy,
                         big_discretionary_buy=big_discretionary_buy,
                         ceo_buy=ceo_buy,
                         sell_on_weakness=sell_on_weakness,
                         cluster_sell=cluster_sell,
                         big_discretionary_sell=big_discretionary_sell,
                         ceo_sell=ceo_sell,
                         total_transactions=total_transactions,
                         significant=significant,
                         mixed_signals=mixed_signals,
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
