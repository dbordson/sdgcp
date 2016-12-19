import os
from sdapp.models import IssuerCIK, FTPFileList, FullForm
import urllib2
import sys
from datetime import date

cwd = os.getcwd()
today = date.today()

# For reference
# except:
#     e = sys.exc_info()[0]
#     print "Error: %s" % e
#     print "Cannot connect"
#     print "Check emailaddress.txt file or EMAIL_ADDRESS global variable"
#     print "And check your internet connection"
#
#     exit(0)


def httpsdownload(url):
    try:
        urlobj = urllib2.urlopen(url)
        data = urlobj.read()
        return data

    except:
        print "Can't get file in ", url


def extractcik(fullpath):
    try:
        return fullpath[:fullpath.find('/')]
    except:
        return 'ERROR'


def saveandclear(formsforsave):
    if len(formsforsave) > 0:
        FullForm.objects.bulk_create(formsforsave)
    formsforsave = []
    return formsforsave


cik_num_list = IssuerCIK.objects.values_list('cik_num', flat=True)

allforms = set(FullForm.objects.values_list('sec_path',
                                            flat=True))

try:
    filelistobjects = FTPFileList.objects.all()
    filestring = filelistobjects[len(filelistobjects) - 1].files
    filelist = filestring.split(',')
    if filestring == u'':
        secfileset = set()
    else:
        secfileset = set(filelist)
except:
    print 'SEC download list is absent or improperly formed; ',
    print 'check FTPFileList table in database'
    exit(0)

formdownloadset = secfileset - (secfileset & allforms)
print len(secfileset)
print len(allforms)
print len(formdownloadset)
formdownloadlist = list(formdownloadset)
print formdownloadlist

formsforsave = []
count = 0.0
totalformslength = float(len(formdownloadlist))
for formpath in formdownloadlist:
    url = 'https://www.sec.gov/Archives/edgar/data/' + formpath
    text = httpsdownload(url)
    a = FullForm(sec_path=formpath,
                 save_date=today,
                 issuer_cik_num=extractcik(formpath),
                 text=text)
    count += 1.0
    percentcomplete = round(count / totalformslength * 100, 2)
    sys.stdout.write("\r%s / %s forms to scrape : %.2f%%" %
                     (int(count), int(totalformslength),
                      percentcomplete))
    sys.stdout.flush()

    if text is not None:
        formsforsave.append(a)
    if len(formsforsave) > 1000:  # 10 mb
        print '\nSaving a batch',
        formsforsave = saveandclear(formsforsave)
        print 'done with this batch, starting next batch'

print '\nSaving'
formsforsave = saveandclear(formsforsave)
print 'Done with all listed files'
