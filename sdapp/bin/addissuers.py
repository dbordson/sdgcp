import requests
import sys

from sdapp.models import SecurityPriceHist, IssuerCIK
# This requires requests, which can be installed via pip using "pip install
# requests" (http://docs.python-requests.org/en/latest/user/install/#install
# for info)


def CIKFind(ticker):
    # This grabs the CIK for a ticker from the SEC website search bar for
    # finding filings by typing in the ticker.  Returns None if it doesn't
    # work.
    ticker = ticker.replace('.', '')
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
    print 'Linking unlinked SecurityPriceHist objects to IssuerCIK objects',
    print 'and creating any new IssuerCIK objects...'
    print '    Sorting, linking and saving...',
    unlinked_tickers = SecurityPriceHist.objects.filter(issuer=None)
    # finds un
    count = 0.0
    looplength = len(unlinked_tickers)
    for entry in unlinked_tickers:
        print entry.ticker_sym,
        cik_num = int(CIKFind(str(entry.ticker_sym)))
        if not IssuerCIK.objects.filter(cik_num=cik_num).exists():
            new_issuer_cik = IssuerCIK(cik_num=cik_num)
            new_issuer_cik.save()
        entry.issuer_id = cik_num
        entry.save()
        # Counter
        count += 1.0
        percentcomplete = round(count / looplength * 100, 2)
        sys.stdout.write("\r%s / %s forms to parse: %.2f%%" %
                         (int(count), int(looplength),
                          percentcomplete))
        sys.stdout.flush()

    print 'done.'


def newtickers():
    print 'Adding any new SecurityPriceHist objects...'
    print '    Sorting and building...',
    tickers_to_add = []
    with open('sdapp/tickerstoadd.txt') as infile:
        for line in infile:
            ticker_to_add = str(line.strip())
            if not SecurityPriceHist.objects.filter(ticker_sym=ticker_to_add)\
                    .exists():
                tickers_to_add.append(
                    SecurityPriceHist(ticker_sym=ticker_to_add))
    print 'saving...',
    SecurityPriceHist.objects.bulk_create(tickers_to_add)
    print 'done.'


newtickers()
newciks()
