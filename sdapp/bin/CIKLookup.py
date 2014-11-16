from sdapp.models import SecurityPriceHist, IssuerCIK
import requests
# This requires requests, which can be installed via pip using "pip install
# requests" (http://docs.python-requests.org/en/latest/user/install/#install
# for info)


def CIKFind(ticker):
    # This grabs the CIK for a ticker from the SEC website search bar for
    # finding filings by typing in the ticker.  Returns None if it doesn't
    # work.
    url = ('http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=%s&o' +
           'wner=exclude&Find=Find+Companies&action=getcompany') % ticker
    starttag = 'CIK='
    endtag = '&amp'

    try:
        response = requests.get(url)
        CIKstart = response.text.find(starttag)
        CIKend = response.text.find(endtag, CIKstart)
        ciknum = response.text[CIKstart + len(starttag):CIKend]
    except:
        ciknum = None

    if len(ciknum) > 11:
        print 'Search did not work for:', ticker
        print '    Returned', ciknum, 'instead.'
        ciknum = None
    return ciknum


def newciks():
    print 'Linking unlinked tickers to IssuerCIK objects and creating any',
    print 'new IssuerCIK objects...'
    print '    Sorting, linking and saving...',
    unlinked_tickers = SecurityPriceHist.objects.filter(issuer=None)
    # finds un
    for entry in unlinked_tickers:
        print entry.ticker_sym,
        cik_num = int(CIKFind(str(entry.ticker_sym)))
        if not IssuerCIK.filter(cik_num=cik_num).exists():
            new_issuer_cik = IssuerCIK(cik_num=cik_num)
            new_issuer_cik.save()
        entry.issuer_id = cik_num
        entry.save()
    print 'done.'


newciks()
