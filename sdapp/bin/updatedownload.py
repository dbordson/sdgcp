import datetime
import os
import urllib2

# from django.db.models import Max
# from django.utils import timezone

from sdapp.models import IssuerCIK, FTPFileList, SECDayIndex
from sdapp.bin import addissuers
from sdapp.bin.globals import today, update_lookback_days

cwd = os.getcwd()

# Notes:
#
# 1. If you want to stop this program, be mindful of the implications of
#    stopping a download in progress.  The best thing to do is to figure out
#    what could have been downloading and delete it.  Partially downloaded
#    files may raise unexpected exceptions or cause us to fail to capture data.
#
# 2. If you get a 550 error, record the error and send it to me.


def isfloat(data):
    try:
        a = float(data)
        a = True
    except:
        a = False
    return a


def cikfinder(line):
    cikstart = line.find('edgar/data/') + len('edgar/data/')
    cikend = line.find('/', cikstart)
    return line[cikstart:cikend]


def formfinder(line):
    formstart = 0
    formend = line.find(' ')
    return line[formstart:formend]


def filepathfinder(line):
    filepathstart = line.find("edgar/data/") + len('edgar/data/')
    filepathend = len(line)
    return line[filepathstart:filepathend].rstrip()


def download_and_store(indexdate, downloadedindexes):
    qdate = indexdate
    qyear = str(qdate.year)
    qQTR = str((qdate.month - 1)//3 + 1)
    urldate = datetime.date.strftime(indexdate, "%Y%m%d")
    parenturl = "https://www.sec.gov/Archives/edgar/daily-index/" + qyear +\
        "/QTR" + qQTR + "/"
    try:
        parenturlobj = urllib2.urlopen(parenturl)

    except urllib2.URLError as e:
        if e.code == 404:
            print 'No index available for ', urldate, '...'
            return downloadedindexes
        else:
            print 'Connection error for:', parenturl
            return downloadedindexes
    parentdata = parenturlobj.read()
    if "form." + urldate + ".idx" in parentdata:
        print 'Downloading index for ', urldate, '...'
        url = "https://www.sec.gov/Archives/edgar/daily-index/" + qyear +\
            "/QTR" + qQTR + "/form." + urldate + ".idx"
        urlobj = urllib2.urlopen(url)
        data = urlobj.read()
        indexname = "form." + urldate + ".idx"
        SECDayIndex(indexname=indexname, indexcontents=data).save()
        downloadedindexes.append(indexname)
        return downloadedindexes
    else:
        print 'No index available for ', urldate, '...'
        return downloadedindexes


def updatedownload(latest_dayindex_name, latest_db_index_date,
                   recentstoredindexdates):
    print "Connecting to SEC HTTPS site..."
    # Compare list of recent index dates to lookback dates to check.
    dates_to_check = []
    for x in range(0, update_lookback_days + 1):
        testdate = today - datetime.timedelta(x)
        if datetime.date.strftime(testdate, "%Y%m%d") not in \
                recentstoredindexdates:
            dates_to_check.append(testdate)

    if len(dates_to_check) == 0:
        print "No new indexes to download"
    downloadedindexes = []
    for indexdate in dates_to_check:
        downloadedindexes = download_and_store(indexdate, downloadedindexes)

    print "Creating the list of needed forms from any new indices..."
    # note that trailing spaces are important here.
    searchformlist = ['4  ', '3  ', '5  ', '4/A', '3/A', '5/A']
    CIKsInit = IssuerCIK.objects.values_list('cik_num', flat=True)

    LastCIK = '911911911911911911911911911'
    secfileset = set()
    for indexname in downloadedindexes:
        indexcontents = SECDayIndex.objects.get(indexname=indexname)\
            .indexcontents.split('\n')
        print '...' + indexname + '...'
        for line in indexcontents:
            if 'edgar/data/' in line\
                    and line[:3] in searchformlist\
                    and int(cikfinder(line)) == LastCIK:
                formfilename = filepathfinder(line)
                secfileset.add(formfilename)
            elif 'edgar/data/' in line\
                    and line[:3] in searchformlist\
                    and int(cikfinder(line)) in CIKsInit:
                LastCIK = int(cikfinder(line))
                formfilename = filepathfinder(line)
                secfileset.add(formfilename)
        LastCIK = '911911911911911911911911911'
    print 'new list generated.'
    secfilestring = ','.join(secfileset)
    print "Deleting old lists of form filepaths..."
    FTPFileList.objects.all().delete()
    print 'Saving ...'
    FTPFileList(files=secfilestring).save()
    return


print "Downloading new form indices and source forms..."

dindexdirectory = cwd
# CHECK THIS
dindexbasepath = "/edgar/daily-index"

# latest_dayindex_date_time =\
#     SECDayIndex.objects.aggregate(Max('timestamp'))['timestamp__max']
secdayindexobjects =\
    SECDayIndex.objects.order_by('-indexname')
if secdayindexobjects.exists():
    latest_dayindex_name = secdayindexobjects[0].indexname
    datetstring = latest_dayindex_name[5:13]
    latest_db_index_date =\
        datetime.datetime.strptime(datetstring, '%Y%m%d').date()

    recentstoredindexnames = \
        secdayindexobjects.values_list('indexname', flat=True)[0:11]
    recentstoredindexdates = []
    for name in recentstoredindexnames:
        recentstoredindexdates.append(name[5:13])

else:
    latest_dayindex_name = None
    latest_db_index_date = None
    recentstoredindexdates = []

updatedownload(latest_dayindex_name, latest_db_index_date,
               recentstoredindexdates)
print 'Done'
