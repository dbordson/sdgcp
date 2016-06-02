# import datetime
from ftplib import FTP
import os
import sys
import time
# try:
    # import cStringIO as sio
# except ImportError:
import StringIO as sio

from gcloud import storage

from sdapp.bin import addissuers
from sdapp.bin.globals import indexyearlookback, nowUTC, today
from hellodjango.settings import PROJECT_ID, CLOUD_STORAGE_BUCKET

# from sdapp.bin import addissuers
# from sdapp.bin.globals import indexyearlookback
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


def cikfinder(line):
    cikstart = line.find('edgar/data/') + len('edgar/data/')
    cikend = line.find('/', cikstart)
    return line[cikstart:cikend]


def filepathfinder(line):
    filepathstart = line.find("edgar/data/") + len('edgar/data/')
    filepathend = len(line)
    return line[filepathstart:filepathend].rstrip()


def ftplogin():
    try:
        time.sleep(1)
        if os.environ.get('EMAIL_ADDRESS') is None:
            from emailaddress import email
        else:
            email = os.environ.get('EMAIL_ADDRESS')
        ftp = FTP('ftp.sec.gov', 'anonymous', email, '', 120)
        # ftp = FTP('ftp.sec.gov')
        # ftp.login('anonymous', email)
        print "Connected"
        return ftp
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        print "Cannot connect"
        print "Check emailaddress.txt file or EMAIL_ADDRESS global variable"
        print "And check your internet connection"
        # RUN FUNCTION TO QUIT AND EMAIL ERROR
#
#
# class Reader:
#     def __init__(self):
#         self.data = ""

#     def __call__(self, s):
#         self.data += s


def ftpdownload(filepath, local_filename, ftp, bucket):
    try:
        targetfilename = 'temp.txt'
        target = open(targetfilename, 'wb')
        ftp.retrbinary('RETR %s' % filepath, target.write)
        target.close()
        # r = Reader()
        # ftp.retrbinary('RETR %s' % filepath, r)
        blob = bucket.blob(local_filename)
        blob.upload_from_filename(targetfilename,
                                  content_type='text/plain')
        os.remove(targetfilename)
        # blob.upload_from_string(r.data, content_type='text/plain')
    except:
        print "Can't get file in ", filepath


def downloadindices(
        storedquarterlist, qindexbasepath, bucket):
    thisyear = today.year
    print "Connecting to SEC FTP site..."
    ftp = ftplogin()
    # LOAD LIST OF STORED INDICES. IF ANY ARE OMITTED FROM THE LIST, DOWNLOAD
    ftp.cwd(qindexbasepath)
    print "now in /edgar/full-index directory"
    rawindexyearlist = []
    indexyearlist = []
    ftp.retrlines('nlst', rawindexyearlist.append)
    for entry in rawindexyearlist:
        if len(entry) == 4 and entry.isdigit()\
                and int(entry) >= thisyear - indexyearlookback:
            indexyearlist.append(entry)
    #
    # Replacing latest index stored (bc/ updated daily by SEC)
    if len(storedquarterlist) > 0:
        print 'Replacing latest stored index'
        year = storedquarterlist[-1][:4]
        quarter = storedquarterlist[-1][5]
        ftp.cwd(qindexbasepath + "/" + year + "/QTR" + quarter)
        sourcename = "form.idx"
        local_filename = year + "Q" + quarter + ".txt"
        ftpdownload(sourcename, local_filename, ftp, bucket)
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
                print year + 'Q' + quarter[3] + "..."
                indexdirectory = qindexbasepath + "/" + year + "/" + quarter
                sourcename = "form.idx"
                local_filename = year + "Q" + quarter[3] + ".txt"
                ftpdownload(indexdirectory + '/' + sourcename, local_filename,
                            ftp, bucket)
    ftp.close()
    print "Done with index file download attempt"
    return


def generateFTPFileList(storedquarterfilenames, bucket):
    # note trailing spaces.
    searchformlist = ['4  ', '3  ', '5  ', '4/A', '3/A', '5/A']

    CIKsInit = IssuerCIK.objects.values_list('cik_num', flat=True)

    print "Now generating the list of forms we need from the indices we have."

    LastCIK = '911911911911911911911911911'
    secfileset = set()

    for indexfilename in storedquarterfilenames:
        print '...' + indexfilename
        downloadblob = bucket.blob(indexfilename)
        targetfilename = 'temp.txt'
        target = open(targetfilename, 'wb')
        target.close()
        downloadblob.download_to_filename(targetfilename)

        with open(targetfilename) as infile:
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
        os.remove(targetfilename)
        LastCIK = '911911911911911911911911911'
    # endsignal = u'\nEOF_EOF_EOF'
    # for indexfilename in storedquarterfilenames:
        # print '...' + indexfilename
        # downloadblob = bucket.blob(indexfilename)
        # indexstring =\
        #     downloadblob.download_as_string() + endsignal
        # stringlinesobject = sio.StringIO(indexstring)
        # while True:
        #     line = stringlinesobject.readline()
        #     if line == 'EOF_EOF_EOF':
        #         break

        #     if 'edgar/data/' in line\
        #             and line[:3] in searchformlist\
        #             and int(cikfinder(line)) == LastCIK:
        #         formfilename = filepathfinder(line)
        #         secfileset.add(formfilename)

        #     elif 'edgar/data/' in line\
        #             and line[:3] in searchformlist\
        #             and int(cikfinder(line)) in CIKsInit:
        #         LastCIK = int(cikfinder(line))
        #         formfilename = filepathfinder(line)
        #         secfileset.add(formfilename)

        # LastCIK = '911911911911911911911911911'

    'new list generated.'
    secfilestring = ','.join(secfileset)
    print "Deleting old lists of form filepaths..."
    FTPFileList.objects.all().delete()
    print 'Saving ...'
    FTPFileList(files=secfilestring).save()
    return


print "Downloading new form indices and source forms..."
client = storage.Client(project=PROJECT_ID)
bucket = client.get_bucket(CLOUD_STORAGE_BUCKET)

qindexbasepath = "/edgar/full-index"
download = 0


storedfiles = []
storedfileslistiterator = bucket.list_blobs()

for blob in storedfileslistiterator:
    storedfiles.append({'name': blob.name, 'updated': blob.updated})

storedquarterlist = []
storedquarterfilenames = []
latestdl = None
for file in storedfiles:
    if file['name'].endswith('.txt') and file['name'][4] == 'Q':
        storedquarterlist.append(file['name'][:6])
        if latestdl is not None:
            latestdl = max(latestdl, file['updated'])
        else:
            latestdl = file['updated']
        storedquarterfilenames.append(file['name'])


datestringtoday = today.strftime('%Y%m%d')
if latestdl is None:
    print 'Running index download function'
    downloadindices(
        storedquarterlist, qindexbasepath, bucket)
else:
    td = nowUTC - latestdl
    hourslapsed = float(td.seconds) / float(3600)
    if hourslapsed > float(0):
        print 'Running index download function'
        downloadindices(
            storedquarterlist, qindexbasepath, bucket)
    else:
        print 'Already updated indices today. Skipping index download.'


print 'Now updating FTPFileList object.'
generateFTPFileList(storedquarterfilenames, bucket)
print 'Done'
