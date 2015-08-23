import datetime
from ftplib import FTP
import os
import sys
import time

from sdapp.bin import addissuers
from sdapp.models import IssuerCIK, FTPFileList

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


def ftpdownload(filepath, local_filename, ftp):
    try:
        target = open(local_filename, 'wb')
        ftp.retrbinary('RETR %s' % filepath, target.write)
        target.close()
    except:
        print "Can't get file in ", filepath


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


def downloadindices(storedquarterlist):
    print "Connecting to SEC FTP site..."
    ftp = ftplogin()
    # LOAD LIST OF STORED INDICES. IF ANY ARE OMITTED FROM THE LIST, DOWNLOAD
    ftp.cwd(qindexbasepath)
    print "now in /edgar/full-index directory"
    rawindexyearlist = []
    indexyearlist = []
    ftp.retrlines('nlst', rawindexyearlist.append)
    for entry in rawindexyearlist:
        if len(entry) == 4 and entry.find('.') == -1:
            indexyearlist.append(entry)
    #
    # Replacing latest index stored (bc/ updated daily by SEC)
    if len(storedquarterlist) > 0:
        print 'Replacing latest stored index'
        year = storedquarterlist[-1][:4]
        quarter = storedquarterlist[-1][5]
        ftp.cwd(qindexbasepath + "/" + year + "/QTR" + quarter)
        sourcename = "form.idx"
        local_filename = (qindexdirectory + year + "Q" + quarter + ".txt")
        ftpdownload(sourcename, local_filename, ftp)
    #
    print "Now going to go one level deeper and begin to save any missing",
    print "indices..."
    for year in indexyearlist:
        quarterlist = []
        ftp.cwd(qindexbasepath + "/" + year)
        ftp.retrlines('nlst', quarterlist.append)
        for quarter in quarterlist:
            if len(quarter) < 5 and quarter.startswith('QTR') and\
                    not year + 'Q' + quarter[3] in storedquarterlist:
                print (year + 'Q' + quarter[3], "...")
                indexdirectory = qindexbasepath + "/" + year + "/" + quarter
                sourcename = "form.idx"
                local_filename =\
                    qindexdirectory + year + "Q" + quarter[3] + ".txt"
                ftpdownload(indexdirectory + '/' + sourcename, local_filename,
                            ftp)
    ftp.close()
    print "Done with index file download attempt"
    target = open(qindexdirectory + lastdownloadfilename, 'w')
    print>>target, "lastdl = '" + datestringtoday + "'"
    target.close()
    print 'Updated download date storage file.'
    return


def generateFTPFileList(qindexfilelist, qindexdirectory):
    # note trailing spaces.
    searchformlist = ['4  ', '3  ', '5  ', '4/A', '3/A', '5/A']

    CIKsInit = IssuerCIK.objects.values_list('cik_num', flat=True)
    # LOAD A LIST OF ALL INDEXES FROM GOOGLE DRIVE
    # for filename in os.listdir(qindexdirectory):
    #     if filename.endswith('.txt'):
    #         qindexfilelist.append(qindexdirectory + filename)
    # IF FAILS, QUIT AND SEND EMAIL NOTING ERROR

    print "Now genrating the list of forms we need from the indices we have."

    LastCIK = '911911911911911911911911911'
    secfileset = set()
    for index in qindexfilelist:
        # will need to change below line to work with google drive
        with open(qindexdirectory + index) as infile:
            print '...' + index
            for line in infile:
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
    'new list generated.'
    secfilestring = ','.join(secfileset)
    print "Deleting old lists of form filepaths..."
    FTPFileList.objects.all().delete()
    print 'Saving ...'
    FTPFileList(files=secfilestring).save()
    return

print "Downloading new form indices and source forms..."

qindexfilelist = []

qindexbasepath = "/edgar/full-index"
download = 0

qindexfolder = '/qindex/'
qindexdirectory = cwd + qindexfolder
if not(os.path.exists(qindexdirectory)):
    print 'Error, /qindex/ directory missing.'
    print 'If building locally, add /qindex/'
    print 'Also, do not attempt to run this script in Heroku. Exiting...'
    exit(0)

# Check for presence of file storing last download date.
lastdownloadfilename = 'lastdl.py'
if not(os.path.exists(qindexdirectory + lastdownloadfilename)):
    target = open(qindexdirectory + lastdownloadfilename, 'w')
    print>>target, 'lastdl = None'
    target.close()
    print 'Added download date storage file.'

from qindex.lastdl import lastdl

qindexfilelist = []
storedquarterlist = []

for filename in os.listdir(qindexdirectory):
    if filename.endswith('.txt'):
        qindexfilelist.append(filename)
        storedquarterlist.append(filename[:6])

datestringtoday = datetime.date.today().strftime('%Y%m%d')
if lastdl != datestringtoday:
    print 'Running index download function'
    downloadindices(storedquarterlist)
else:
    print 'Already updated indices today. Skipping index download function.'

print 'Now updating FTPFileList object.'
generateFTPFileList(qindexfilelist, qindexdirectory)
print 'Done'

# THIS IS NOT USED, BUT SCRIPT WOULD BE SIMPLER IF DOWNLOADED 2 FLAT SETS AND
# COMPARED THEM.  THE TWO SETS ARE THE SEC FILES AND THE GOOGLE FILES
# files_to_download = \
#     sec_index_file_list - (sec_index_file_list & drive_index_list)
# FOR THIS TO BE REALLY CLEAN WOULD WANT TO GRAB LIST OF INDICES ON FTP
# SITE IN A SINGLE COMMAND, WHICH MIGHT BE ANNOYING TO DO.
