from django.shortcuts import (render_to_response, get_object_or_404,
                              RequestContext, HttpResponseRedirect)
from sdapp.models import (Security, Signal, IssuerCIK, SecurityPriceHist,
                          Form345Entry, PersonHoldingView, SecurityView)
from django.db.models import Q
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
# from django.core.context_processors import csrf
# import datetime


# def check_auth(request):
#     if request.user.is_authenticated():
#         return True
#     else:
#         messagetext = \
#             'Login required for access'
#         messages.success(request, messagetext)
#         return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@login_required()
def options(request, ticker):
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
    issuer_name = Form345Entry.objects.filter(issuer_cik=issuer)\
        .latest('filedatetime').issuer_name
    signals = Signal.objects.filter(issuer=issuer)\
        .order_by('-signal_date')
    return render_to_response('sdapp/options.html',
                              {'ticker': ticker,
                               'issuer_name': issuer_name,
                               'signals': signals},
                              context_instance=RequestContext(request),
                              )


# def pricedetail(request, ticker):
#     SPH_obj = SecurityPriceHist.objects.filter(ticker_sym=ticker)[0]

#     pricelist = ClosePrice.objects.filter(SecurityPriceHist=SPH_obj)
#     return render_to_response('sdapp/pricedetail.html',
#                               {'pricelist': pricelist})


# class filterscreens(ListView):

#     # c = {}
#     # c.update(csrf(request))

#     template_name = 'sdapp/filterscreens.html'
#     context_object_name = 'screens'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(filterscreens, self).dispatch(*args, **kwargs)

#     def get_queryset(self):
#         print self
#         self.issuer = get_object_or_404(IssuerCIK, cik_num=self.args[0])
#         return Signal.objects.filter(issuer=self.issuer)


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
        
#         entry_query = get_query(query_string, ['title', 'body',])
        
#         found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

#     return render_to_response('search/search_results.html',
#                           { 'query_string': query_string, 'found_entries': found_entries },
#                           context_instance=RequestContext(request))


def filterintermed(request):
    cik_num = request.POST.get('cik_num', '')
    print cik_num
    if cik_num is not '':
        return HttpResponseRedirect('/sdapp/screens/' + cik_num + '/')
    else:
        return HttpResponseRedirect('/sdapp/screens/')
# is_int(request.GET['q'].strip()) and\


@login_required()
def screens(request):
    # print request
    query_string = None
    found_entries = None
    signal_types = []
    dbuyactive = True
    wbuyactive = True
    ticker = None
    num_of_records = None
    # print 'q', request.GET['q']
    # print ('q' in request.GET)
    # print request.GET['q'] == ''
    # print 'dbuy', 'discretionarybuy' in request.GET
    if ('q' in request.GET):
        query_string = request.GET['q'].strip()
        dbuyactive = False
        wbuyactive = False

    if 'selectbox' in request.GET\
            and 'discretionarybuy' in request.GET.getlist('selectbox'):
        print 'discretionarybuy'
        print request.GET['selectbox']
        signal_types.append('Discretionary Buy')
        dbuyactive = True

    if 'selectbox' in request.GET\
            and 'buyonweakness' in request.GET.getlist('selectbox'):
        print 'buyonweakness'
        print request.GET['selectbox']
        signal_types.append('Discretionary Buy after a Decline')
        wbuyactive = True

    # THE BELOW COMMENTED CODE WOULD BE USED FOR THE TOGGLE BUTTON
    # CHECKBOXES IN THE SCREENS.HTML TEMPLATE INSTEAD OF THE ABOVE
    # if 'discretionarybuy' in request.GET:
    #     signal_types.append('Discretionary Buy')
    #     dbuyactive = True
    #     # print 'discretionarybuy', request.GET['discretionarybuy'].strip()
    # if 'buyonweakness' in request.GET:
    #     signal_types.append('Discretionary Buy after a Decline')
    #     wbuyactive = True
    #     # print 'buyonweakness', request.GET['buyonweakness'].strip()

    if ('q' in request.GET) and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper()).exists() and\
            SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper())[0]\
            .issuer is not None:
        ticker = request.GET['q'].strip().upper()
        issuer = SecurityPriceHist.objects\
            .filter(ticker_sym=query_string.upper())[0].issuer
        found_entries = \
            Signal.objects.filter(signal_name__in=signal_types)\
            .filter(issuer=issuer).order_by('-signal_date')
        num_of_records = found_entries.count()
    elif ('q' in request.GET) and\
            request.GET['q'].strip() == '':
        query_string = ' '
        # print 'here'
        # print 'query_string', query_string, '.'
        # print signal_types
        found_entries = \
            Signal.objects.filter(signal_name__in=signal_types)\
            .order_by('-signal_date')
        num_of_records = found_entries.count()
        # print found_entries

    return render_to_response('sdapp/screens.html',
                              {'found_entries': found_entries,
                               'query_string': query_string,
                               'dbuyactive': dbuyactive,
                               'wbuyactive': wbuyactive,
                               'ticker': ticker,
                               'num_of_records': num_of_records},
                              context_instance=RequestContext(request),
                              )


@login_required()
def discretionarybuy(request):
    signal_name_1 = 'Discretionary Buy'
    signal_name_2 = 'Discretionary Buy after a Decline'
    qs = Signal.objects\
        .filter(Q(signal_name=signal_name_1) |
                Q(signal_name=signal_name_2))\
        .order_by('-signal_date')

    return render_to_response('sdapp/discretionarybuy.html',
                              {'signals': qs},
                              context_instance=RequestContext(request),
                              )


@login_required()
def weaknessbuy(request):
    signal_name = 'Discretionary Buy after a Decline'
    qs = Signal.objects\
        .filter(signal_name=signal_name)\
        .order_by('-signal_date')

    return render_to_response('sdapp/weaknessbuy.html',
                              {'signals': qs},
                              context_instance=RequestContext(request),
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
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk},
                              context_instance=RequestContext(request),)


@login_required()
def holdingdetail(request, ticker):
    headtitle = 'Current Holdings'
    security_obj = \
        Security.objects.get(ticker=ticker)
    issuer = security_obj.issuer
    issuer_pk = security_obj.issuer.pk
    entrylist = Form345Entry.objects\
        .filter(issuer_cik_id=issuer_pk)\
        .filter(supersededdt=None)\
        .order_by('reporting_owner_cik', 'security', '-filedatetime')
    return render_to_response('sdapp/formentrydetail.html',
                              {'headtitle': headtitle,
                               'entrylist': entrylist,
                               'ticker': ticker,
                               'issuer': issuer,
                               'issuer_pk': issuer_pk},
                              context_instance=RequestContext(request),)


@login_required()
def byperson(request, ticker):
    issuer = \
        Security.objects.get(ticker=ticker).issuer
    personviews = PersonHoldingView.objects.filter(issuer=issuer)\
        .order_by('person_name', '-intrinsic_value')
    return render_to_response('sdapp/personviews.html',
                              {'ticker': ticker,
                               'issuer_pk': issuer.pk,
                               'personviews': personviews},
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
    common_stock_security = \
        Security.objects.get(ticker=ticker)
    issuer = common_stock_security.issuer
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
                               'deriv_table': deriv_table},
                              context_instance=RequestContext(request),
                              )


# def holdingtable(request, ticker):
#     issuer = \
#         IssuerCIK.objects.filter(SecurityPriceHist__ticker_sym=ticker_sym)[0]
#     lookbackdays = 365 * 100
#     startdate = datetime.date.today() - datetime.timedelta(lookbackdays)
#     affiliationset = Affiliation.objects.filter(issuer=issuer)\
#         .filter(most_recent_filing__gte=startdate)
#     holdingset = HoldingType.objects.filter(issuer=issuer)\
#         .filter(affiliation__in=affiliationset).order_by('owner')\
#         .exclude(units_held=0.0).exclude(units_held=None)
#     stockholdingset = holdingset.filter(deriv_or_nonderiv='N')
#     stockholdingtitles = list(set(stockholdingset
#                               .values_list('security_title', flat=True)
#                               .distinct()))
#     totalset = AggHoldingType.objects.filter(issuer=issuer)\
#         .exclude(units_held=None)
#     stocktotals = totalset.filter(deriv_or_nonderiv='N')
#     stockholdinglists = []
#     for title in stockholdingtitles:
#         stockholdinglist = []
#         stockholdinglist.append(title)
#         titleholdings = stockholdingset.filter(security_title=title)\
#             .order_by('-units_held')[:5]
#         # print titleholdings.values_list('owner', flat=True)
#         stockholdinglist.append(titleholdings)

#         total = stocktotals.filter(security_title=title)[0]
#         stockholdinglist.append(total)
#         stockholdinglists.append(stockholdinglist)
#         # print title
#         # print stockholdinglist

#     derivholdingset = holdingset.filter(deriv_or_nonderiv='D')
#     derivholdingtitles = list(set(derivholdingset
#                               .values_list('security_title', flat=True)
#                               .distinct()))
#     derivtotals = totalset.filter(deriv_or_nonderiv='D')
#     derivholdinglists = []
#     for title in derivholdingtitles:
#         derivholdinglist = []
#         derivholdinglist.append(title)
#         titleholdings = derivholdingset.filter(security_title=title)\
#             .order_by('-units_held')[:5]
#         derivholdinglist.append(titleholdings)
#         total = derivtotals.filter(security_title=title)[0]
#         derivholdinglist.append(total)
#         derivholdinglists.append(derivholdinglist)
#     # print stockholdinglists
#     return render_to_response('sdapp/holdingtable.html',
#                               {'ticker_sym': ticker_sym,
#                                'startdate': startdate,
#                                'stockholdingtitles': stockholdingtitles,
#                                'affiliationset': affiliationset,
#                                'stockholdinglists': stockholdinglists,
#                                'derivholdinglists': derivholdinglists})

@login_required()
def personholdingtable(request, ticker, owner):
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
