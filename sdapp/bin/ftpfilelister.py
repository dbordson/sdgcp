import os
from sdapp.models import IssuerCIK, FTPFileList


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

print "Building a list of form filepaths..."

cik_num_set = set(IssuerCIK.objects.values_list('cik_num', flat=True))
formset = set(['3', '3/A', '4', '4/A', '5', '5/A'])

qindexdirectory = os.path.expanduser('~/AutomatedFTP/QFilingIndices/')
if not(os.path.exists(qindexdirectory)):
    os.makedirs(qindexdirectory)
    print "Created a directory: ", qindexdirectory

qindexfilelist = []
for filename in os.listdir(qindexdirectory):
    if filename.endswith('.txt'):
        qindexfilelist.append(qindexdirectory + filename)

secfileset = set()
for index in qindexfilelist:
    with open(index) as infile:
        print '...for ' + index + ' ...'
        for line in infile:
            if 'edgar/data/' in line and\
                    cikfinder(line) in cik_num_set and\
                    formfinder(line) in formset:
                formfilename = filepathfinder(line)
                secfileset.add(formfilename)
secfilestring = ','.join(secfileset)
print 'Saving ...'
FTPFileList(files=secfilestring).save()
print 'Done'
