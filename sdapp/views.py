from django.shortcuts import render_to_response
from sdapp.models import CompanyStockHist, ClosePrice, IssuerCIK,\
    Form345Entry, Affiliation, Holding
import datetime


def options(request, ticker_sym):
    tickersym = ticker_sym
    return render_to_response('sdapp/options.html',
                              {'tickersym': tickersym})


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
                              {'affiliationlist': affiliationlist})


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
        .filter(affiliation__in=affiliationset).order_by('owner')
    stockholdingset = holdingset.filter(deriv_or_nonderiv='N')
    stockholdingtitles = stockholdingset.values('security_title').distinct()

    derivholdingset = holdingset.filter(deriv_or_nonderiv='D')
    derivholdingtitles = stockholdingset.values('security_title').distinct()
    return render_to_response('sdapp/holdingtable.html',
                              {'startdate': startdate,
                               'affiliationset': affiliationset,
                               'stockholdingset': stockholdingset,
                               'stockholdingtitles': stockholdingtitles,
                               'derivholdingset': derivholdingset,
                               'derivholdingtitles': derivholdingtitles})

