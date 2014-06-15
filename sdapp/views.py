from django.shortcuts import render_to_response
from sdapp.models import CompanyStockHist, ClosePrice


def detail(request, ticker_sym):
    stockid = CompanyStockHist.objects.filter(ticker_sym=ticker_sym)[0]
    pricelist = ClosePrice.objects.filter(companystockhist=stockid)
    return render_to_response('sdapp/detail.html',
                              {'pricelist': pricelist})
