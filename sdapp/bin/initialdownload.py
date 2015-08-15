import datetime
from ftplib import FTP
import os
import sys
import time

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


def quitandemail(error):
    return
    # DEFINE FUNCTION TO QUIT AND SEND EMAIL NOTING ERROR


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


def ftpdownload(filepath, local_filename):
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


print "Downloading new form indices and source forms..."

qindexfilelist = []
qindexdirectory = cwd + '/QFilingIndices/'
qindexbasepath = "/edgar/full-index"
dindexdirectory = cwd + '/DFilingIndices/'
download = 0


authenticated = False
# AUTHENTICATE INTO GOOGLE DRIVE HERE
if authenticated is False:  # REPLACE THIS STATEMENT WHEN ABOVE CODE FILLED IN
    error = 'initialdownload.py failed to authenticate with Google Drive'
    quitandemail(error)

# WRITE SCRIPT HERE TO GET LATEST INDEX FROM GOOGLE?/AMZN S3? AND SEE
# WHEN IT WAS DOWNLOADED


direxists = False
# if THE DIRECTORY DOES NOT EXIST:
# QUIT AND SEND EMAIL STATING ERROR THAT DIRECTORY DOES NOT EXIST
if direxists is False:  # REPLACE THIS STATEMENT WHEN ABOVE CODE FILLED IN
    error = 'initialdownload.py failed.  Proper Google Drive dir is absent'
    quitandemail(error)

print "Connecting to SEC FTP site..."
ftp = ftplogin()

google_drive_download_success = False

drive_index_list = set(['filepath1', 'filepath2', 'filepath3'])
if google_drive_download_success is False:
    error = 'initialdownload.py failed.  Google Drive download failed'
    quitandemail(error)
if not(os.path.exists(dindexdirectory)):
    os.makedirs(dindexdirectory)
    print "Created a directory: ", dindexdirectory

# note trailing spaces.
searchformlist = ['4  ', '3  ', '5  ', '4/A', '3/A', '5/A']

CIKsInit = IssuerCIK.objects.values_list('cik_num', flat=True)

# GET DATE OF MOST RECENT INDEX FROM DRIVE HERE
most_recent_index_date_time = 101010101010
twelve_hours_ago = datetime.datetime.now() - datetime.timedelta(.5)
if most_recent_index_date_time < twelve_hours_ago:
    # IF LATEST INDEX FILE IS MORE THAN THAN 12 HOURS OLD, DELETE IT.
    # (WILL DOWNLOAD MISSING FILES IN A MINUTE, SO WILL BE REPLACED)
    return

# LOAD A LIST OF ALL INDEX FILES.  IF ANY ARE OMITTED FROM THE LIST, DOWNLOAD
ftp.cwd(qindexbasepath)
print "now in /edgar/full-index directory"
rawindexyearlist = []
indexyearlist = []
ftp.retrlines('nlst', rawindexyearlist.append)
for entry in rawindexyearlist:
    if len(entry) < 5 and isfloat(entry):
        indexyearlist.append(entry)
print "Now going to go one level deeper and begin to save any missing",
print "indices..."

for year in indexyearlist:
    quarterlist = []
    ftp.cwd(qindexbasepath + "/" + year)
    ftp.retrlines('nlst', quarterlist.append)
    for quarter in quarterlist:
        # FIGURE OUT WHAT quarter[3] IS
        if len(quarter) < 5 and quarter.startswith('QTR') and\
                not any(existingindex.find(year + 'Q' + quarter[3] + '.txt')
                        != -1 for existingindex in qindexfilelist):
            print (year + 'Q' + quarter[3], "...")
            indexdirectory = qindexbasepath + "/" + year + "/" + quarter
            sourcename = "form.idx"
            local_filename = (os.getcwd() + year + "Q" + quarter[3] + ".txt")
            # Next we save the file in the ephemeral dyno environment
            ftpdownload(indexdirectory + '/' + sourcename, local_filename)
            # Next we upload the file to google drive for safekeeping
            # NOW MOVE THIS FILE FROM TEMP STORAGE TO GOOGLE DRIVE
ftp.close()
print "Done with index file download attempt"

# THIS IS NOT USED, BUT SCRIPT WOULD BE SIMPLER IF DOWNLOADED 2 FLAT SETS AND
# COMPARED THEM.  THE TWO SETS ARE THE SEC FILES AND THE GOOGLE FILES
# files_to_download = \
#     sec_index_file_list - (sec_index_file_list & drive_index_list)


# LOAD A LIST OF ALL INDEXES FROM GOOGLE DRIVE
qindexfilelist = ['1', '2', '3']  # pull call indexes from drive, in order?
# for filename in os.listdir(qindexdirectory):
#     if filename.endswith('.txt'):
#         qindexfilelist.append(qindexdirectory + filename)
# IF FAILS, QUIT AND SEND EMAIL NOTING ERROR

print "Now lets generate the list of forms we need from the indices we have."

LastCIK = '911911911911911911911911911'
secfileset = set()
for index in qindexfilelist:
    # will need to change below line to work with google drive
    with open(index) as infile:
        print '... ' + index,
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
print 'Done'
