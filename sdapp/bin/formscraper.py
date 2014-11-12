import os
from sdapp.models import IssuerCIK, Form345Entry, FTPFileList, FullForm
from ftplib import FTP
from StringIO import StringIO
import sys
from datetime import date

cwd = os.getcwd()
today = date.today()


def ftplogin():
    try:
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
        print "Cannot connect"
        exit(0)


# def ftprefresh(ftp):
#     try:
#         ftp.voidcmd('NOOP')
#         return ftp
#     except IOError as e:
#         print "I/O error({0}): {1}".format(e.errno, e.strerror)
#         print "Retrying..."
#         ftp = ftplogin()
#         ftp.voidcmd('NOOP')
#         print "Worked!"
#         return ftp


def ftpdownload(filepath, ftp):
    try:
        r = StringIO()
        ftp.retrbinary('RETR %s' % filepath, r.write)
        return r.getvalue()

    except:
        try:
            ftp = ftplogin()
            r = StringIO()
            ftp.retrbinary('RETR %s' % filepath, r.write)
            return r.getvalue()
        except:
            print "Can't get file in ", filepath


def extractcik(fullpath):
    try:
        return fullpath[:fullpath.find('/')]
    except:
        return 'ERROR'


def saveandclear(formsforsave):
    FullForm.objects.bulk_create(formsforsave)
    formsforsave = []
    return formsforsave


if not(os.path.isfile('emailaddress.txt')) and\
        os.environ.get('EMAIL_ADDRESS') is None:
    print "Let's locally store your email address as an ftp password",
    print "(you won't be logged in yet)."
    target = open(cwd + '/' + 'emailaddress.txt', 'w')
    print "Created an email address storage file in", cwd + '/' + \
        'emailaddress.txt'
    print "What is your email address? (for anonymous ftp password)"
    email = raw_input()
    print>>target, email
    target.close()
    print ''


cik_num_list = IssuerCIK.objects.values_list('cik_num', flat=True)

allforms = set(Form345Entry.objects.values_list('sec_path',
                                                flat=True))

try:
    filelistobjects = FTPFileList.objects.all()
    filestring = filelistobjects[len(filelistobjects) - 1].files
    filelist = filestring.split(',')
    secfileset = set(filelist)
except:
    print 'SEC download list is absent or improperly formed; ',
    print 'check FTPFileList table in database'
    exit(0)

formdownloadset = secfileset - (secfileset & allforms)
formdownloadlist = list(formdownloadset)


ftp = ftplogin()
formsforsave = []
count = 0.0
looplength = float(len(formdownloadlist))
for formpath in formdownloadlist:
    fullpath = '/edgar/data/' + formpath
    text = ftpdownload(fullpath, ftp)
    a = FullForm(sec_path=formpath,
                 save_date=today,
                 issuer_cik_num=extractcik(formpath),
                 text=text)
    if float(int(10*count/looplength)) !=\
            float(int(10*(count-1)/looplength)):
        print int(count/looplength*100), 'percent'
    count += 1.0
    formsforsave.append(a)
    if sys.getsizeof(formsforsave) > 10000000:  # 10 mb
        print 'Saving'
        formsforsave = saveandclear(formsforsave)
        print 'Done with this batch, starting next batch'

print 'Saving'
formsforsave = saveandclear(formsforsave)
print 'Done with all listed files'
