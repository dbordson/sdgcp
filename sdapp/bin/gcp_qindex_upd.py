# import datetime
import gzip
import os
from StringIO import StringIO
import re
import urllib2
# try:
# import cStringIO as sio
# except ImportError:
# import StringIO as sio

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
# 2. If you get a 550 error, record the error and send it to me.


def cikfinder(line):
    cikstart = line.find('edgar/data/') + len('edgar/data/')
    cikend = line.find('/', cikstart)
    return line[cikstart:cikend]


def filepathfinder(line):
    filepathstart = line.find("edgar/data/") + len('edgar/data/')
    filepathend = len(line)
    return line[filepathstart:filepathend].rstrip()


def generatestoredfileinfo():
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
    return storedquarterlist, storedquarterfilenames, latestdl

def httpsdownload(url, local_filename, bucket):
    try:
        urlobj = urllib2.urlopen(url)
        buf = StringIO(urlobj.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()

        targetfilename = 'temp.txt'
        target = open(targetfilename, 'w')
        target.write(data)
        target.close()

        blob = bucket.blob(local_filename)
        blob.upload_from_filename(targetfilename,
                                  content_type='text/plain')
        os.remove(targetfilename)
        # blob.upload_from_string(r.data, content_type='text/plain')
    except:
        print "Can't get file in ", url


def downloadindices(storedquarterlist, qindexbasepath, bucket):
    thisyear = today.year
    print "Accessing SEC HTTPS site..."
    # LOAD LIST OF STORED INDICES. IF ANY ARE OMITTED FROM THE LIST, DOWNLOAD

    print "now in /edgar/full-index directory"

    url = "https://www.sec.gov/Archives/edgar/full-index/"
    urlobj = urllib2.urlopen(url)
    data = urlobj.read()
    tag = '<img class="img_icon" src="/icons/folder.gif" alt="folder icon">'
    years = []
    for m in re.finditer(tag, data):
        year = data[m.end():m.end()+4]
        if int(year) >= thisyear - indexyearlookback:
            years.append(data[m.end():m.end()+4])

    #
    # Replacing latest index stored (bc/ updated daily by SEC)
    if len(storedquarterlist) > 0:
        print 'Replacing latest stored index'
        year = storedquarterlist[-1][:4]
        quarter = storedquarterlist[-1][5]
        local_filename = year + "Q" + quarter + ".txt"
        url = "https://www.sec.gov/Archives/edgar/full-index/" + year +\
            "/QTR" + quarter + "/form.gz"
        httpsdownload(url, local_filename, bucket)
    #
    print "Now going to go one level deeper and begin to save any missing",
    print "indices..."
    # Scrapes available quarters for each year.  Then pulls index for each QTR.
    for year in years:
        quarters = []
        url = 'https://www.sec.gov/Archives/edgar/full-index/' + year + '/'
        urlobj = urllib2.urlopen(url)
        data = urlobj.read()
        tag = '/icons/folder.gif" alt="folder icon">'
        for m in re.finditer(tag, data):
            quarters.append(data[m.end()+3:m.end()+4])
        for quarter in quarters:
            url = "https://www.sec.gov/Archives/edgar/full-index/" + year +\
                "/QTR" + quarter + "/form.gz"

            if len(quarter) < 5 and\
                    not year + 'Q' + quarter in storedquarterlist:
                print year + 'Q' + quarter + "..."
                local_filename = year + "Q" + quarter + ".txt"
                httpsdownload(url, local_filename, bucket)
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

storedquarterlist, storedquarterfilenames, latestdl = \
    generatestoredfileinfo()

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

# Update stored file info based on post-download status.
storedquarterlist, storedquarterfilenames, latestdl = \
    generatestoredfileinfo()

print 'Now updating FTPFileList object.'
generateFTPFileList(storedquarterfilenames, bucket)
print 'Done'
