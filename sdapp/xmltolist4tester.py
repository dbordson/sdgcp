
import json
import os
import xmlmanager
import xmltolist4


# This code will work best if the stored files are in a subdirectory of
# the current working directory.
dropboxdir = os.path.expanduser('~/Dropbox')

print "test"

#Here the program begins
print "Welcome to the nonderivative transaction parser"

if not(os.path.isfile(dropboxdir + '/AutomatedFTP/CIKs.txt')):
    target = open(dropboxdir + '/AutomatedFTP/CIKs.txt', 'w')
    print>>target, '882095'
    target.close()
CIKs = []
with open(dropboxdir + '/AutomatedFTP/CIKs.txt') as infile:
    for line in infile:
        CIKs.append(line.strip())
print "Using CIKs:", CIKs
print " "

print "What Form? (3, 4, 4/A, 5)"
print "Also, just press enter for form 4"
form = raw_input()
if form == "":
    form = '4'
print "We'll work with form", form

ndxnlist = []
dxnlist = []
i = 0
ndxncounter = 0
dxncounter = 0
bothcounter = 0
eithercounter = 0
notcounter = 0
parseerrorlist = []
totaldirectorylength = 0

for CIK in CIKs:
    xmlfiledirectory = xmlmanager.filemapper(CIK, form)
    #Here is the magic where we call the xnparser,
    totaldirectorylength += len(xmlfiledirectory)
    #nullxnlist = ([], [])

    for xmlfile in xmlfiledirectory:
        try:
            newxnlist = xmltolist4.formtestandparse(xmlfile)
            ndxnlist += newxnlist[0]
            dxnlist += newxnlist[1]
            if newxnlist[0] != []:
                ndxncounter += 1
            if newxnlist[1] != []:
                dxncounter += 1
            if (newxnlist[0] != []) and (newxnlist[1] != []):
                bothcounter += 1
            if (newxnlist[0] != []) or (newxnlist[1] != []):
                eithercounter += 1
            if (newxnlist[0] == []) and (newxnlist[1] == []):
                notcounter += 1
                #newerrorchecker = xmltolist4.xn4parse(xmlfile)
                #nullxnlist += newerrorchecker
                #if newerrorchecker[0] != [] or newerrorchecker[1] != []:
                #   print xmlfile

            i += 1
        except:
            parseerrorlist.append(xmlfile)
meanlist = []
for item in ndxnlist:
    meanlist.append(item[13])
if meanlist[0] == 'plh':
    meanlist = [0]
print float(sum(meanlist))
print len(meanlist)
print "average", float(sum(meanlist)) / len(meanlist)

print "The total number of files reviewed was:", totaldirectorylength
print "how many times did the for loop run?"
print i
print "bothcounter", bothcounter
print "eithercounter", eithercounter
print "no reported positions", notcounter
#print "nullxnlist", nullxnlist
print "how many times did we add to the deriv and nonderiv item lists"
print ndxncounter, dxncounter
print "So what did the parser give us, let's print an indication"
print "Here is the length of the non-derivative item list: ",
print len(ndxnlist)
print "Here is the length of the derivative item list: ",
print len(dxnlist)
# print ndxnlist[1][2]
print "Length of error list indicating omitted files:", len(parseerrorlist)
print "Here are any files from above that were filed in 2005 or later:"
oldyears = ['94', '95', '96', '97', '98', '99', '00', '01', '02', '03', '04']
for line in parseerrorlist:
    if not any(line.find('-' + oldyear + '-') != -1 for oldyear in oldyears):
        print line

print "Let's save these entries"
#NonDeriv xn file for John C. Martin

# for entry in ndxnlist:
    #

if form == '4' or form == '4/A' or form == '5':
    i = 0
    if form == '4':
        target = open("parseresults/NonDerivXn4File.txt", 'w')
        legend = open("parseresults/NonDerivLegend4.txt", 'w')
    if form == '4/A':
        target = open("parseresults/NonDerivXn4AFile.txt", 'w')
        legend = open("parseresults/NonDerivLegend4A.txt", 'w')
    if form == '5':
        target = open("parseresults/NonDerivXn5File.txt", 'w')
        legend = open("parseresults/NonDerivLegend5.txt", 'w')

    target.truncate()
    print>>legend, """NonDerivative Transaction List Key:
    [0] = Period Of Report
    [1] = Issuer CIK
    [2] = Reporting Owner CIK
    [3] = Reporting Owner Name
    [4] = Is the Reporting Owner a Director?
    [5] = Is the Reporting Owner an Officer?
    [6] = Is the Reporting Owner a Ten Percent Owner?
    [7] = Is the Reporting Owner Something Else?
    [8] = Reporting Owner Officer Title
    [9] = Security Title
    [10] = Placeholder Cell
    [11] = Transaction Date
    [12] = Transaction Code
    [13] = Shares in Transaction
    [14] = Transaction Price Per Share
    [15] = Transaction Acquired/Disposed Code
    [16] = Placeholder Cell
    [17] = Placeholder Cell
    [18] = Placeholder Cell
    [19] = Shares Owned Following Transaction
    [20] = Direct Or Indirect Ownership
    [21] = 1 if a "10b5-1" footnote is present
    [22] = Nonderivative Transaction Number (on that Form 4)
    [23] = Source File Name/Partial Path
    [24] = (form 5 only) Not Subject To Section 16
    [25] = (form 5 only) Form 3 Holdings Reported
    [26] = (form 5 only) Form 4 Transactions Reported
    [27] = Form Type

    """
    legend.close()
    json.dump(ndxnlist, target)
    print len(ndxnlist)
    target.close()

    if form == '4':
        target = open("parseresults/DerivXn4File.txt", 'w')
        legend = open("parseresults/DerivLegend4.txt", 'w')
    if form == '4/A':
        target = open("parseresults/DerivXn4AFile.txt", 'w')
        legend = open("parseresults/DerivLegend4A.txt", 'w')
    if form == '5':
        target = open("parseresults/DerivXn5File.txt", 'w')
        legend = open("parseresults/DerivLegend5.txt", 'w')

    target.truncate()
    print>>legend, """Derivative Transaction List Key:
    [0] = Period Of Report
    [1] = Issuer CIK
    [2] = Reporting Owner CIK
    [3] = Reporting Owner Name
    [4] = Is the Reporting Owner a Director?
    [5] = Is the Reporting Owner an Officer?
    [6] = Is the Reporting Owner a Ten Percent Owner?
    [7] = Is the Reporting Owner Something Else?
    [8] = Reporting Owner Officer Title
    [9] = Security Title
    [10] = Conversion Price
    [11] = Transaction Date
    [12] = Transaction Code
    [13] = Shares in Transaction
    [14] = Transaction Price Per Share
    [15] = Transaction Acquired/Disposed Code
    [16] = Expiration Date
    [17] = Underlying Security Title
    [18] = Underlying Security Shares
    [19] = Shares Owned Following Transaction
    [20] = Direct Or Indirect Ownership
    [21] = 1 if a "10b5-1" footnote is present
    [22] = Derivative Transaction Number (on that Form 4)
    [23] = Source File Name/Partial Path
    [24] = (form 5 only) Not Subject To Section 16
    [25] = (form 5 only) Form 3 Holdings Reported
    [26] = (form 5 only) Form 4 Transactions Reported
    [27] = Form Type

    """
    legend.close()

    json.dump(dxnlist, target)
    print len(dxnlist)
    #print j
    target.close()


if form == '3':
    i = 0
    target = open("parseresults/NonDeriv3File.txt", 'w')
    target.truncate()
    legend = open("parseresults/NonDerivLegend3.txt", 'w')
    print>>legend, """NonDerivative Transaction List Key:
    [0] = Period Of Report
    [1] = Issuer CIK
    [2] = Reporting Owner CIK
    [3] = Reporting Owner Name
    [4] = Is the Reporting Owner a Director?
    [5] = Is the Reporting Owner an Officer?
    [6] = Is the Reporting Owner a Ten Percent Owner?
    [7] = Is the Reporting Owner Something Else?
    [8] = Reporting Owner Officer Title
    [9] = Security Title
    [10] = Placeholder Cell
    [11] = Placeholder Cell
    [12] = Placeholder Cell
    [13] = Placeholder Cell
    [14] = Placeholder Cell
    [15] = Placeholder Cell
    [16] = Placeholder Cell
    [17] = Placeholder Cell
    [18] = Placeholder Cell
    [19] = Shares Owned Following Transaction
    [20] = Direct Or Indirect Ownership
    [21] = 1 if a "10b5-1" footnote is present
    [22] = Nonderivative Transaction Number (on that Form 4)
    [23] = Source File Name/Partial Path
    [24] = (form 5 only) Not Subject To Section 16
    [25] = (form 5 only) Form 3 Holdings Reported
    [26] = (form 5 only) Form 4 Transactions Reported
    [27] = Form Type

    """
    legend.close()
    json.dump(ndxnlist, target)
    print len(ndxnlist)
    target.close()

    target = open("parseresults/Deriv3File.txt", 'w')
    target.truncate()
    legend = open("parseresults/DerivLegend3.txt", 'w')
    print>>legend, """Derivative Transaction List Key:
    [0] = Period Of Report
    [1] = Issuer CIK
    [2] = Reporting Owner CIK
    [3] = Reporting Owner Name
    [4] = Is the Reporting Owner a Director?
    [5] = Is the Reporting Owner an Officer?
    [6] = Is the Reporting Owner a Ten Percent Owner?
    [7] = Is the Reporting Owner Something Else?
    [8] = Reporting Owner Officer Title
    [9] = Security Title
    [10] = Conversion Price
    [11] = Placeholder Cell
    [12] = Placeholder Cell
    [13] = Placeholder Cell
    [14] = Placeholder Cell
    [15] = Placeholder Cell
    [16] = Expiration Date
    [17] = Underlying Security Title
    [18] = Underlying Security Shares
    [19] = Placeholder Cell
    [20] = Direct Or Indirect Ownership
    [21] = 1 if a "10b5-1" footnote is present
    [22] = Derivative Transaction Number (on that Form 4)
    [23] = Source File Name/Partial Path
    [24] = (form 5 only) Not Subject To Section 16
    [25] = (form 5 only) Form 3 Holdings Reported
    [26] = (form 5 only) Form 4 Transactions Reported
    [27] = Form Type

    """
    legend.close()
    json.dump(dxnlist, target)
    print len(dxnlist)
    #print j
    target.close()




# In case you have a hard time starting up the program, here is what
# the output looks like:

#[['2014-01-02', '0000882095', '0001190578', 'MARTIN JOHN C',
# 'Common Stock', '2014-01-02', 'M', 140625, 8.005, 'A', 4197746],
# ['2014-01-02', '0000882095', '0001190578', 'MARTIN JOHN C',
# 'Common Stock', '2014-01-02', 'S', 140625, 75.0235, 'D',
# 4057121]]

#This drops the code into lists of lists (it looks like
#sometimes people call these 2d lists)
#5 minutes of research indicates that this may be fairly
#Straightforward to put into mysql, but I have not learned
#much about it yet, so I don't know if that will be done
#as easily as I just said it.
