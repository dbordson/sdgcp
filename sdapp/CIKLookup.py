from sdapp.models import CompanyStockHist, CIK
import requests
# This requires requests, which can be installed via pip using "pip install
# requests" (http://docs.python-requests.org/en/latest/user/install/#install
# for info)


def CIKFind(ticker):

    url = 'http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=%s&owner=exclude&Find=Find+Companies&action=getcompany' % ticker
    starttag = 'CIK='
    endtag = '&amp'

    try:
        response = requests.get(url)
        CIKstart = response.text.find(starttag)
        CIKend = response.text.find(endtag, CIKstart)
        ciknum = response.text[CIKstart + len(starttag):CIKend]
    except:
        ciknum = 'ACCESS ERROR'

    if len(ciknum) > 11:
        ciknum = 'NO CIK FOUND'

    return ciknum


def newciks():
    for entry in CompanyStockHist.objects.all():
        print entry
        try:
            entry.cik
            pass
        except:
            CIKnum = CIKFind(str(entry.ticker_sym))
            d = CIK(cik_num=CIKnum, companystockhist=entry)
            d.save()


newciks()
