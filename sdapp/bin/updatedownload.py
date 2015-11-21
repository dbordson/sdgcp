import datetime
from ftplib import FTP
import os
import sys
import time

from django.db.models import Max
from django.utils import timezone

from sdapp.models import IssuerCIK, FTPFileList, SECDayIndex
from sdapp.bin import addissuers
from sdapp.bin.globals import date_of_any_new_filings

cwd = os.getcwd()

# Notes:
#
# 1. If you want to stop this program, be mindful of the implications of
#    stopping a download in progress.  The best thing to do is to figure out
#    what could have been downloading and delete it.  Partially downloaded
#    files may raise unexpected exceptions or cause us to fail to capture data.
#
# 2. If you get a 550 error from ftplib, record the error and send it to me.
#    Unfortunately, sometimes these errors are an issue with the server on the
#    other side. Because of how this script runs, if you get this error, you
#    may find blank files in the form 4 storage sections.  Check for these
#    occassionally.  Also, if you get such an error/find empty storage files
#    delete the empty files and re-run the program.  Definitely let me know
#    if you get the error twice in a row, since that indicates a problem on our
#    side.


def ftplogin():
    try:
        time.sleep(1)
        if os.environ.get('EMAIL_ADDRESS') is None:
            target = open(cwd + '/' + 'emailaddress.txt')
            email = target.read()
            email = email.strip()
            target.close()
        else:
            email = os.environ.get('EMAIL_ADDRESS')
        ftp = FTP('ftp.sec.gov')
        ftp.login('anonymous', email)
        print "Connected"
        return ftp
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        print "Cannot connect"
        print "Check emailaddress.txt file or EMAIL_ADDRESS global variable"
        print "And check your internet connection"
        # RUN FUNCTION TO QUIT AND EMAIL ERROR


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


def updatedownload(latest_dayindex_name):
    print "Connecting to SEC FTP site..."
    ftp = ftplogin()

    # note that trailing spaces are important here.
    searchformlist = ['4  ', '3  ', '5  ', '4/A', '3/A', '5/A']

    CIKsInit = IssuerCIK.objects.values_list('cik_num', flat=True)

    # LOAD A LIST OF ALL INDEX FILES.  GET THE FILES MORE RECENT THAN IN THE DB
    # OR IF THERE ARE NO DAILY INDICES IN THE DB, SAVE ONLY THE LATEST INDEX
    ftp.cwd(dindexbasepath)
    print "now in /edgar/daily-index directory"

    indexdaylist = []
    contentslist = []
    ftp.retrlines('nlst', contentslist.append)
    for entry in contentslist:
        if entry[:5] == 'form.' and entry[-4:] == '.idx':
            indexdaylist.append(entry)
    indexdaylist.sort(reverse=True)
    indexesfordownload = []
    if latest_dayindex_name is None:
        indexesfordownload = indexdaylist[:10]
    else:
        # pull up to 10 most recent indexes.
        for indexname in indexdaylist[:10]:
            if indexname > latest_dayindex_name:
                indexesfordownload.append(indexname)
    if len(indexesfordownload) == 0:
        print "No new indexes available"
    else:
        print "Now going to go one level deeper and begin to save any missing",
        print "indices..."

        for index in indexesfordownload:
            filepath = dindexbasepath + "/" + index
            textofindexes = []

            def handle_binary(more_data):
                textofindexes.append(more_data)

            resp = ftp.retrbinary('RETR %s' % filepath, callback=handle_binary)
            print resp
            textofindexes = ''.join(textofindexes)
            SECDayIndex(indexname=index, indexcontents=textofindexes).save()

    ftp.close()

    print "Creating the list of needed forms the update indices..."

    LastCIK = '911911911911911911911911911'
    secfileset = set()
    for indexname in indexesfordownload:
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
    if latest_dayindex_name[:5] == 'form.' \
            and latest_dayindex_name[13:] == '.idx':
        datetstring = latest_dayindex_name[5:13]
        latest_db_index_date =\
            datetime.datetime.strptime(datetstring, '%Y%m%d').date()
    else:
        latest_db_index_date = None
else:
    latest_dayindex_name = None
    latest_db_index_date = None
if latest_db_index_date is not None\
        and date_of_any_new_filings <= latest_db_index_date:
    print "Last index created at:", latest_db_index_date
    print 'FTPFileList already up to date. No update indices to download.'
else:
    updatedownload(latest_dayindex_name)
    print 'Done'
