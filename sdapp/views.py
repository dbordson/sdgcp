from django.shortcuts import render_to_response
from sdapp.models import CompanyStockHist, ClosePrice, IssuerCIK,\
    Form345Entry, Affiliation, Holding
import datetime


def options(request, ticker_sym):
    return render_to_response('sdapp/options.html',
                              {'ticker_sym': ticker_sym})


def pricedetail(request, ticker_sym):
    stockid = CompanyStockHist.objects.filter(ticker_sym=ticker_sym)[0]

    pricelist = ClosePrice.objects.filter(companystockhist=stockid)
    return render_to_response('sdapp/pricedetail.html',
                              {'pricelist': pricelist})


def formentrydetail(request, ticker_sym):
    # stockid = CompanyStockHist.objects.get(ticker_sym=ticker_sym)
    cikforticker = \
        IssuerCIK.objects.filter(companystockhist__ticker_sym=ticker_sym)[0]
    cikidforticker = cikforticker.cik_num
    entrylist = Form345Entry.objects.filter(issuer_cik_id=cikidforticker)
    # pricelist = ClosePrice.objects.filter(companystockhist=stockid)
    return render_to_response('sdapp/entrydetail.html',
                              {'entrylist': entrylist,
                               'cikforticker': cikforticker,
                               'cikidforticker': cikidforticker})


def affiliationdetail(request, ticker_sym):
    # stockid = CompanyStockHist.objects.get(ticker_sym=ticker_sym)
    issuer = \
        IssuerCIK.objects.filter(companystockhist__ticker_sym=ticker_sym)[0]
    affiliationlist = Affiliation.objects.filter(issuer=issuer).\
        order_by('-most_recent_filing')
    return render_to_response('sdapp/affiliationdetail.html',
                              {'ticker_sym': ticker_sym,
                               'affiliationlist': affiliationlist})


def holdingdetail(request, ticker_sym):
    # stockid = CompanyStockHist.objects.get(ticker_sym=ticker_sym)
    issuer = \
        IssuerCIK.objects.filter(companystockhist__ticker_sym=ticker_sym)[0]
    holdinglist = Holding.objects.filter(issuer=issuer).\
        order_by('owner')
    return render_to_response('sdapp/holdingdetail.html',
                              {'holdinglist': holdinglist})


def holdingtable(request, ticker_sym):
    issuer = \
        IssuerCIK.objects.filter(companystockhist__ticker_sym=ticker_sym)[0]
    lookbackdays = 548
    startdate = datetime.date.today() - datetime.timedelta(lookbackdays)
    affiliationset = Affiliation.objects.filter(issuer=issuer)\
        .filter(most_recent_filing__gte=startdate)
    holdingset = Holding.objects.filter(issuer=issuer)\
        .filter(affiliation__in=affiliationset).order_by('owner')\
        .exclude(units_held=0.0)
    stockholdingset = holdingset.filter(deriv_or_nonderiv='N')
    stockholdingtitles = list(set(stockholdingset
                              .values_list('security_title', flat=True)
                              .distinct()))
    stockholdinglists = []
    for title in stockholdingtitles:
        stockholdinglist = []
        stockholdinglist.append(title)
        titleholdings = stockholdingset.filter(security_title=title)\
            .order_by('-units_held')[:5]
        print titleholdings.values_list('owner', flat=True)
        stockholdinglist.append(titleholdings)
        stockholdinglists.append(stockholdinglist)
        print title
        print stockholdinglist

    derivholdingset = holdingset.filter(deriv_or_nonderiv='D')
    derivholdingtitles = list(set(derivholdingset
                              .values_list('security_title', flat=True)
                              .distinct()))
    derivholdinglists = []
    for title in derivholdingtitles:
        derivholdinglist = []
        derivholdinglist.append(title)
        titleholdings = derivholdingset.filter(security_title=title)\
            .order_by('-units_held')[:5]
        derivholdinglist.append(titleholdings)
        derivholdinglists.append(derivholdinglist)
    print stockholdinglists
    return render_to_response('sdapp/holdingtable.html',
                              {'ticker_sym': ticker_sym,
                               'startdate': startdate,
                               'stockholdingtitles': stockholdingtitles,
                               'affiliationset': affiliationset,
                               'stockholdinglists': stockholdinglists,
                               'derivholdinglists': derivholdinglists})


def individualaffiliation(request, ticker_sym, reporting_owner_cik_num):
    issuer = \
        IssuerCIK.objects.filter(companystockhist__ticker_sym=ticker_sym)[0]
    affiliation = Affiliation.objects.filter(
        reporting_owner_cik_num=reporting_owner_cik_num)[0]
    holdinglist = Holding.objects.filter(affiliation=affiliation).\
        order_by('-most_recent_xn')
    return render_to_response('sdapp/individualaffiliation.html',
                              {'ticker_sym': ticker_sym,
                               'affiliation': affiliation,
                               'issuer': issuer,
                               'holdinglist': holdinglist})
