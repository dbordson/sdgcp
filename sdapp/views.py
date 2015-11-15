import datetime
from decimal import Decimal
from math import sqrt
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
# from django.db.models import Sum
from django.db.models import Q
from django.shortcuts import (render_to_response, redirect,
                              RequestContext, HttpResponseRedirect)
from django.template.defaulttags import register

from sdapp.bin import update_affiliation_data
from sdapp.bin.globals import (perf_period_days_td, buy_on_weakness,
                               cluster_buy, discretionary_buy, today,
                               sell_on_strength, cluster_sell,
                               discretionary_sell, now, sel_person_id)
from sdapp.models import (Affiliation, Form345Entry, PersonHoldingView,
                          PersonSignal, Security, SecurityView, SigDisplay,
                          SecurityPriceHist, WatchedName)
from sdapp.misc.filingcodes import filingcodes, acq_disp_codes
from sdapp import holdingbuild


@register.filter
def multiply(a, b):
    return a * b


@register.filter
def negate(value):
    return -value


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def mean(lst):
    # """calculates mean"""
    lstsum = Decimal(0)
    for i in range(len(lst)):
        lstsum += lst[i]
    return (lstsum / len(lst))


def stddev(lst):
    # """calculates standard deviation"""
    lstsum = Decimal(0)
    mn = mean(lst)
    for entry in lst:
        lstsum += pow((entry - mn), 2)
    return sqrt(lstsum / Decimal(len(lst) - 1))


def dotproduct(four_column_table):
    dotprod = sum(Decimal(r) * Decimal(s) for p, q, r, s in four_column_table)
    return dotprod


def js_readable_date(some_datetime_object):
    timetuple = some_datetime_object.timetuple()
    timestamp = time.mktime(timetuple)
    return timestamp * 1000.0


# converts date to datetime, but ignores None
def nd(dt):
    try:
        return dt.date()
    except:
        return dt


def appendif(startlist, newitem):
    if newitem is None:
        return startlist
    else:
        startlist.append(newitem)
        return startlist


def index(request):
    sphset = SecurityPriceHist.objects.exclude(issuer=None)\
        .order_by('ticker_sym')
    for sph in sphset:
        sph.name = sph.issuer.name

    return render_to_response('sdapp/index.html',
                              {'sphset': sphset,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def options(request, ticker):
    ticker = ticker.upper()
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    issuer_name = issuer.name
    # Pulls whether this stock is on the user's watch list
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)

    signal_entries = SigDisplay.objects.filter(issuer=issuer)
    sig_dates = []
    signal_entry = None
    if signal_entries.exists():
        signal_entry = signal_entries[0]
        sig_dates = appendif(sig_dates, signal_entry.bow_first_sig_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.db_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.sos_first_sig_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.ds_detect_date)
    sig_highlights = []
    for sig_date in sig_dates:
        sig_highlights.append(
            [js_readable_date(sig_date + datetime.timedelta(-5)),
             js_readable_date(sig_date + datetime.timedelta(5))])
    if len(sig_highlights) != 0:
        sig_persons = \
            list(PersonSignal.objects.filter(issuer=issuer)
                 .filter(significant=True)
                 .exclude(reporting_person=None)
                 .values_list('reporting_person',
                              'reporting_person__person_name')
                 .distinct())
    else:
        sig_persons = []
    holding_affiliations = Affiliation.objects.filter(issuer=issuer)\
        .exclude(share_equivalents_value=None)\
        .filter(is_active=True)\
        .order_by('-share_equivalents_value')[:3]
    persons_data =\
        list(holding_affiliations
             .values_list('reporting_owner', 'person_name'))\
        + sig_persons
    graph_data_json, titles_json, ymax =\
        holdingbuild.buildgraphdata(issuer, ticker, persons_data)
    perf_period = -perf_period_days_td.days

    latest_price = update_affiliation_data.get_price(issuer, today)

    # This only exists to preserve selected persons when the user
    # clicks back and forth among tabs with a person selected
    if sel_person_id in request.GET \
            and request.GET[sel_person_id] != 'None':
        selected_person = int(request.GET[sel_person_id])
    else:
        selected_person = None

    return render_to_response('sdapp/options.html',
                              {'graph_data_json': graph_data_json,
                               'holding_affiliations': holding_affiliations,
                               'issuer_name': issuer_name,
                               'latest_price': latest_price,
                               'perf_period': perf_period,
                               'sel_person_id': sel_person_id,
                               'selected_person': selected_person,
                               'sig_highlights': sig_highlights,
                               'signal_entry': signal_entry,
                               'titles_json': titles_json,
                               'ticker': ticker,
                               'watchedname': watchedname,
                               'ymax': ymax,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def drilldown(request, ticker):
    ticker = ticker.upper()
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    issuer_name = issuer.name
    # Pulls whether this stock is on the user's watch list
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)

    signal_entries = SigDisplay.objects.filter(issuer=issuer)

    sig_dates = []
    signal_entry = None
    if signal_entries.exists():
        signal_entry = signal_entries[0]
        sig_dates = appendif(sig_dates, signal_entry.bow_first_sig_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.db_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.sos_first_sig_detect_date)
        sig_dates = appendif(sig_dates, signal_entry.ds_detect_date)
    sig_highlights = []
    for sig_date in sig_dates:
        sig_highlights.append(
            [js_readable_date(sig_date + datetime.timedelta(-5)),
             js_readable_date(sig_date + datetime.timedelta(5))])
    startdate = now - datetime.timedelta(365)

    # Builds transaction queryset
    if sel_person_id in request.GET \
            and request.GET[sel_person_id] != 'None':

        selected_person = int(request.GET[sel_person_id])
        recententries_qs =\
            Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(filedatetime__gte=startdate)\
            .filter(reporting_owner_cik=selected_person)
    else:
        selected_person = None
        recententries_qs =\
            Form345Entry.objects.filter(issuer_cik=issuer)\
            .filter(filedatetime__gte=startdate)

    recententries =\
        recententries_qs\
        .order_by('-filedatetime', 'transaction_number')\
        .values('filedatetime', 'transaction_number', 'transaction_date',
                'reporting_owner_cik', 'reporting_owner_name',
                'transaction_code', 'xn_acq_disp_code',
                'transaction_shares', 'security_title',
                'xn_price_per_share', 'conversion_price', 'sec_path',
                'form_type', 'reported_shares_following_xn',
                'is_director', 'is_officer', 'is_ten_percent', 'sec_url',
                'entry_internal_id')
    # Creates variable to filter graph by person
    if selected_person is None:
        persons_data =\
            Affiliation.objects.filter(issuer=issuer)\
            .filter(is_active=True)\
            .values_list('reporting_owner', 'person_name')
    else:
        persons_data =\
            Affiliation.objects.filter(issuer=issuer)\
            .filter(reporting_owner=selected_person)\
            .values_list('reporting_owner', 'person_name')

    persons_for_radio =\
        Affiliation.objects.filter(issuer=issuer)\
        .filter(is_active=True)\
        .values('reporting_owner__person_name', 'reporting_owner')\
        .order_by('reporting_owner__person_name').distinct()
    persons_with_data = len(persons_data)
    # builds graph data -- see housingbuild.py for logic
    graph_data_json, titles_json, ymax =\
        holdingbuild.buildgraphdata(issuer, ticker, persons_data)

    # Pick the template to use based on which url is passed
    template_location = 'sdapp/drilldown.html'
    if 'PATH_INFO' in request.META:
        if 'bigchart' in request.META['PATH_INFO']:
            template_location = 'sdapp/bigchart.html'
    # if 'drilldown' in request.GET.

    return render_to_response(template_location,
                              {'acq_disp_codes': acq_disp_codes,
                               'recententries': recententries,
                               'filingcodes': filingcodes,
                               'graph_data_json': graph_data_json,
                               'issuer_name': issuer_name,
                               'persons_for_radio': persons_for_radio,
                               'persons_with_data': persons_with_data,
                               'sel_person_id': sel_person_id,
                               'selected_person': selected_person,
                               'sig_highlights': sig_highlights,
                               'signal_entry': signal_entry,
                               'titles_json': titles_json,
                               'ticker': ticker,
                               'watchedname': watchedname,
                               'ymax': ymax,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def watchtoggle(request):
    issuer = None
    # Handles arrival of request to bounce the user somewhere else
    # if they aren't carrying the right kind of data
    if request.method == "POST"\
            and 'ticker' in request.POST:
        ticker = request.POST['ticker']
        common_stock_security = \
            Security.objects.get(ticker=ticker)
        issuer = common_stock_security.issuer
        watchedname = WatchedName.objects.filter(issuer=issuer)\
            .filter(user__username=request.user.username)
    if issuer is None and 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    elif issuer is None:
        return redirect('/sdapp/')

    if watchedname.exists():
        watchedname.delete()
    else:
        sph = SecurityPriceHist.objects.filter(ticker_sym=ticker)[0]
        sig_disps = SigDisplay.objects.filter(issuer=issuer)
        if sig_disps.exists():
            last_signal_sent = sig_disps.latest('last_signal').last_signal
        else:
            last_signal_sent = None
        WatchedName(user=request.user,
                    issuer=issuer,
                    securitypricehist=sph,
                    ticker_sym=ticker,
                    last_signal_sent=last_signal_sent).save()
    return render_to_response('sdapp/watchtoggle.html',
                              {'watchedname': watchedname,
                               'ticker': ticker,
                               },
                              )


@login_required()
def watchlisttoggle(request, ticker):
    ticker = ticker.upper()
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    if watchedname.exists():
        watchedname.delete()

        if 'HTTP_REFERER' in request.META:
            url = request.META['HTTP_REFERER']
            if url.find('/?') != -1:
                url = url[:url.find('/?')]
            return redirect(url)
        return HttpResponseRedirect('/sdapp/' + str(ticker))
    else:
        sph = SecurityPriceHist.objects.filter(ticker_sym=ticker)[0]
        sig_disps = SigDisplay.objects.filter(issuer=issuer)
        if sig_disps.exists():
            last_signal_sent = sig_disps.latest('last_signal').last_signal
        else:
            last_signal_sent = None
        WatchedName(user=request.user,
                    issuer=issuer,
                    securitypricehist=sph,
                    ticker_sym=ticker,
                    last_signal_sent=last_signal_sent).save()
        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect('/sdapp/' + str(ticker))


def filterintermed(request):
    cik_num = request.POST.get('cik_num', '')
    if cik_num is not '':
        return HttpResponseRedirect('/sdapp/screens/' + cik_num + '/')
    else:
        return HttpResponseRedirect('/sdapp/screens/')


def tickersearch(request):

    if 'ticker' in request.GET\
            and 'HTTP_REFERER' in request.META\
            and request.GET['ticker'].strip() == '':
        messagetext = \
            'Please enter a ticker.'
        messages.success(request, messagetext)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if ('ticker' in request.GET)\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['ticker'].strip().upper()).exists()\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['ticker'].strip().upper())[0]\
            .issuer is not None:
        ticker = request.GET['ticker'].strip().upper()
        return HttpResponseRedirect('/sdapp/' + str(ticker))

    else:
        messagetext = \
            'Ticker Not Found'
        messages.success(request, messagetext)
        return HttpResponseRedirect('/sdapp/')


@login_required()
def screens(request):
    watchlist = \
        WatchedName.objects.filter(user=request.user).order_by('ticker_sym')\
        .annotate()
    watched_names = WatchedName.objects.filter(user=request.user)\
        .values('issuer__pk', 'issuer__name', 'securitypricehist__ticker_sym')
    for watched_name in watched_names:
        signal = SigDisplay.objects.filter(issuer=watched_name['issuer__pk'])
        if signal.exists() and signal[0].last_signal is not None:
            watched_name['last_signal'] = signal[0].last_signal
        else:
            watched_name['last_signal'] = None
    c = {'buy_on_weakness': buy_on_weakness,
         'cluster_buy': cluster_buy,
         'discretionary_buy': discretionary_buy,
         'sell_on_strength': sell_on_strength,
         'cluster_sell': cluster_sell,
         'discretionary_sell': discretionary_sell,
         'watched_names': watched_names,
         'watchlist': watchlist}
    c.update(csrf(request))
    return render_to_response('sdapp/screens.html',
                              c,
                              context_instance=RequestContext(request),
                              )


@login_required()
def searchsignals(request):
    if request.method == "POST":
        search_text = request.POST['search_text'].strip()
    else:
        search_text = ''

    ticker = None
    num_of_records = 0

    qs = SigDisplay.objects.none()

    if 'selectbox' in request.POST:
        # signals = [buy_on_weakness, cluster_buy, discretionary_buy,
            # sell_on_strength, cluster_sell, discretionary_sell]
        signal_count = 0
        if buy_on_weakness in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(buy_on_weakness=None)
            signal_count += 1
        if cluster_buy in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(cluster_buy=None)
            signal_count += 1
        if discretionary_buy in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(discretionary_buy=None)
            signal_count += 1
        if sell_on_strength in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(sell_on_strength=None)
            signal_count += 1
        if cluster_sell in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(cluster_sell=None)
            signal_count += 1
        if discretionary_sell in request.POST.getlist('selectbox'):
            qs = qs | SigDisplay.objects.exclude(discretionary_sell=None)
            signal_count += 1

        if signal_count == 0:
            qs = SigDisplay.objects.all()
    if search_text == '':
        found_entries = qs
    elif ('search_text' in request.POST) and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=search_text.upper()).exists() and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=search_text.upper())[0]\
            .issuer is not None:
        ticker = search_text.upper()
        issuer = SecurityPriceHist.objects\
            .filter(ticker_sym=ticker)[0].issuer
        found_entries = \
            qs.filter(issuer=issuer)
    else:
        found_entries = SigDisplay.objects.none()
    num_of_records = found_entries.count()
    return render_to_response('sdapp/ajax_search.html',
                              {'found_entries': found_entries,
                               'num_of_records': num_of_records,
                               'search_text': search_text,
                               'ticker': ticker,
                               },
                              )


@login_required()
def formentrydetail(request, ticker):
    headtitle = 'All Entries'
    security_obj = \
        Security.objects.get(ticker=ticker)
    issuer = security_obj.issuer
    issuer_pk = security_obj.issuer.pk
    entrylist = Form345Entry.objects.filter(issuer_cik_id=issuer_pk)\
        .order_by('reporting_owner_cik', 'security', '-filedatetime')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


@login_required()
def holdingdetail(request, ticker):
    ticker = ticker.upper()
    headtitle = 'Current Holdings'
    security_obj = \
        Security.objects.get(ticker=ticker)
    issuer = security_obj.issuer
    issuer_pk = security_obj.issuer.pk
    entrylist = Form345Entry.objects\
        .filter(issuer_cik_id=issuer_pk)\
        .filter(supersededdt=None)\
        .order_by('reporting_owner_cik', 'security', '-filedatetime')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


@login_required()
def byperson(request, ticker):
    ticker = ticker.upper()
    issuer = \
        Security.objects.get(ticker=ticker).issuer
    personviews = PersonHoldingView.objects.filter(issuer=issuer)\
        .order_by('person_name', '-intrinsic_value')
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    return render_to_response('sdapp/personviews.html',
                              {'ticker': ticker,
                               'issuer_pk': issuer.pk,
                               'personviews': personviews,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),)


def compile_holdings_into_table(person_view_set, total_view_set,
                                deriv_or_nonderiv):
    sec_ids_titles = \
        total_view_set\
        .filter(deriv_or_nonderiv=deriv_or_nonderiv)\
        .values_list('security', 'short_sec_title').distinct()\
        .order_by('-intrinsic_value')
    holding_lists = []
    for security_id, short_sec_title in sec_ids_titles:
        sec_holdings = person_view_set.filter(security_id=security_id)\
            .order_by('-units_held')[:5]
        total = total_view_set.filter(security=security_id)[0]
        holding_list = [short_sec_title, sec_holdings, total]
        holding_lists.append(holding_list)
    return holding_lists


@login_required()
def holdingtable(request, ticker):
    ticker = ticker.upper()
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    watchedname = WatchedName.objects.filter(issuer=issuer)\
        .filter(user__username=request.user.username)
    issuer_name = Form345Entry.objects.filter(issuer_cik=issuer)\
        .latest('filedatetime').issuer_name

    person_view_set = PersonHoldingView.objects.filter(issuer=issuer)\
        .exclude(units_held=0.0).exclude(units_held=None)

    total_view_set = SecurityView.objects.filter(issuer=issuer)\
        .exclude(units_held=0.0).exclude(units_held=None)
    non_deriv_table = \
        compile_holdings_into_table(person_view_set, total_view_set, 'N')
    deriv_table = \
        compile_holdings_into_table(person_view_set, total_view_set, 'D')
    return render_to_response('sdapp/holdingtable.html',
                              {'ticker': ticker,
                               'issuer_name': issuer_name,
                               'non_deriv_table': non_deriv_table,
                               'deriv_table': deriv_table,
                               'watchedname': watchedname, },
                              context_instance=RequestContext(request),
                              )


@login_required()
def personholdingtable(request, ticker, owner):
    ticker = ticker.upper()
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    latest_form_filed = Form345Entry.objects\
        .filter(issuer_cik=issuer).filter(reporting_owner_cik=owner)\
        .latest('filedatetime')
    person_name = latest_form_filed.reporting_owner_name
    person_title = latest_form_filed.reporting_owner_title
    person_view_set = PersonHoldingView.objects\
        .filter(issuer=issuer).filter(owner=owner)\
        .exclude(units_held=0.0).exclude(units_held=None)
    # These should be reordered by intrinsic economic value, once available
    nonderivativeholdings = person_view_set.filter(deriv_or_nonderiv='N')\
        .order_by('-intrinsic_value', '-units_held')
    derivativeholdings = person_view_set.filter(deriv_or_nonderiv='D')\
        .order_by('-intrinsic_value', '-units_held')

    return render_to_response('sdapp/personholdingtable.html',
                              {'ticker': ticker,
                               'person_name': person_name,
                               'person_title': person_title,
                               'issuer': issuer,
                               'nonderivativeholdings': nonderivativeholdings,
                               'derivativeholdings': derivativeholdings},
                              context_instance=RequestContext(request),
                              )
