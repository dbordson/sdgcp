from sdapp.models import IssuerCIK, Form345Entry
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

cwd = os.getcwd()


def binary_to_boolean(inputbinary):
    if inputbinary == '1':
        return True
    else:
        return False


class e:
    entry_internal_id = None
    period_of_report = None
    issuer_cik = None
    issuer_cik_num = None
    reporting_owner_cik = None
    reporting_owner_cik_num = None
    reporting_owner_name = None
    is_director = None
    is_officer = None
    is_ten_percent = None
    is_something_else = None
    reporting_owner_title = None
    security_title = None
    conversion_price = None
    transaction_date = None
    transaction_code = None
    transaction_shares = None
    xn_price_per_share = None
    xn_acq_disp_code = None
    expiration_date = None
    underlying_title = None
    underlying_shares = None
    shares_following_xn = None
    direct_or_indirect = None
    tenbfive_note = None
    transaction_number = None
    source_name_partial_path = None
    five_not_subject_to_section_sixteen = None
    five_form_three_holdings = None
    five_form_four_transactions = None
    form_type = None
    deriv_or_nonderiv = None
    filedatetime = None
    supersededdt = None


def filemapper(CIK):
    xmldirectory = []
    filedir = os.path.expanduser('~/AutomatedFTP/storage' + str(CIK) + '/')

    for root, dirs, files in os.walk(filedir):
        for file in files:
            if file.endswith('.xml'):
                xmldirectory.append(os.path.join(root, file))
    return xmldirectory


# Extracts text attribute
def t_att(numchar, treeobject, path):
    try:
        a = treeobject.find(path).text[0:numchar]
    except AttributeError:
        a = None

    return a


# Extracts float attribute
def f_att(numdec, treeobject, path):
    try:
        a = round(float(treeobject.find(path).text), numdec)
    except AttributeError:
        a = None

    return a


# Extracts boolean attribute
def b_att(treeobject, path):
    try:
        if treeobject.find(path).text[0:1] == '1':
            a = '1'
        else:
            a = '0'
    except:
        a = '0'

    return a


def path_to_filename(xmlfilename):
    # This function finds the last '/' in the string to extract the filename.
    # The first line is kind of voodoo, but it uses slice notation to take the
    # whole string, but backwards -- this is used because python has no find
    # from the right function.
    last_slash_position = xmlfilename[::-1].find('/')
    return xmlfilename[len(xmlfilename) - last_slash_position:]


def parse(root, child, child2, entrynumber, deriv_or_nonderiv, xmlfilename):
    a = e()
    a.entry_internal_id = None  # FIX
    a.period_of_report = t_att(20, root, 'periodOfReport')
    # a.issuer_cik = SPACER
    a.issuer_cik_num = t_att(10, root, 'issuer/issuerCik')
    # a.reporting_owner_cik = SPACER
    a.reporting_owner_cik_num =\
        t_att(10, root, 'reportingOwner/reportingOwnerId/rptOwnerCik')
    a.reporting_owner_name =\
        t_att(80, root, 'reportingOwner/reportingOwnerId/rptOwnerName')
    a.is_director =\
        b_att(root, 'reportingOwner/reportingOwnerRelationship/isDirector')
    a.is_officer =\
        b_att(root, 'reportingOwner/reportingOwnerRelationship/isOfficer')
    a.is_ten_percent =\
        b_att(root,
              'reportingOwner/reportingOwnerRelationship/isTenPercentOwner')
    a.is_something_else =\
        b_att(root, 'reportingOwner/reportingOwnerRelationship/isOther')
    a.reporting_owner_title =\
        t_att(80, root,
              'reportingOwner/reportingOwnerRelationship/officerTitle')
    a.security_title = t_att(80, child2, 'securityTitle/value')
    a.conversion_price = f_att(4, child2, 'conversionOrExercisePrice/value')
    a.transaction_date = t_att(20, child2, 'transactionDate/value')
    a.transaction_code =\
        t_att(2, child2, 'transactionCoding/transactionCode')
    a.transaction_shares =\
        f_att(4, child2, 'transactionAmounts/transactionShares/value')
    a.xn_price_per_share =\
        f_att(4, child2,
              'transactionAmounts/transactionPricePerShare/value')
    a.xn_acq_disp_code =\
        t_att(2, child2,
              'transactionAmounts/transactionAcquiredDisposedCode/value')
    a.expiration_date = t_att(20, child2, 'expirationDate/value')
    a.underlying_title =\
        t_att(80, child2, 'underlyingSecurity/underlyingSecurityTitle/value')
    a.underlying_shares =\
        f_att(4, child2, 'underlyingSecurity/underlyingSecurityShares/value')
    a.shares_following_xn =\
        f_att(4, child2,
              'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
    a.direct_or_indirect =\
        t_att(2, child2, 'ownershipNature/directOrIndirectOwnership/value')
    a.tenbfive_note = None  # FIX
    a.transaction_number = entrynumber
    a.source_name_partial_path = path_to_filename(xmlfilename)
    a.five_not_subject_to_section_sixteen =\
        t_att(15, root, 'notSubjectToSection16')
    a.five_form_three_holdings = t_att(15, root, 'form3HoldingsReported')
    a.five_form_four_transactions =\
        t_att(15, root, 'form4TransactionsReported')
    a.form_type = \
        t_att(5, root,
              'documentType')
    a.deriv_or_nonderiv = deriv_or_nonderiv
    a.filedatetime = t_att(15, root, 'dateandtime')
    a.supersededdt = None

    pass


def formcrawl(xmlfilename):
    tree = ET.parse(xmlfilename)
    root = tree.getroot()

    # Finds the 10b5-1 footnotes 
    footnotenames = []
    for fnotes in root.findall('footnotes'):
        for fnote in fnotes.findall('footnote'):
            if '10b5-1' in fnote.text:
                footnotenames.append(fnote.get('id'))

    NonDerivEntryNumber = 1
    for child in root.findall('nonDerivativeTable'):
        deriv_or_nonderiv = 'N'
        for child2 in child.findall('nonDerivativeTransaction'):
            entry = parser(root, child, child2, NonDerivEntryNumber,
                           deriv_or_nonderiv, xmlfilename)
            NonDerivEntryNumber += 1



def formentryinsert():
    entries = []
    parseerrorlist = []
    totaldirectorylength = 0
    i = 0
    for CIKentry in IssuerCIK.objects.all():
        xmlfiledirectory = filemapper(CIKentry)
        totaldirectorylength += len(xmlfiledirectory)

        for xmlfile in xmlfiledirectory:
            try:
                newxnlist = xmltolist4.formtestandparse(xmlfile)
                i += 1
            except:
                parseerrorlist.append(xmlfile)
    # meanlist = []
    # for item in ndxnlist:
    #     meanlist.append(item[13])
    # if meanlist[0] is None:
    #     meanlist = [0]
    # print float(sum(meanlist))
    # print len(meanlist)
    # print "average", float(sum(meanlist)) / len(meanlist)

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
    oldyears = ['94', '95', '96', '97', '98', '99',
                '00', '01', '02', '03', '04']
    for line in parseerrorlist:
        if not any(line.find('-' + oldyear + '-') != -1
                   for oldyear in oldyears):
            print line

    print "Let's save these entries"
    #NonDeriv xn file for John C. Martin
    all_entries = Form345Entry.objects.all()
    id_list = []
    for entry in all_entries:
        id_list.append(entry.entry_internal_id)
    existingciks = []
    all_ciks = IssuerCIK.objects.all()
    for entry in all_ciks:
        existingciks.append(entry.cik_num)
    entries = []
    print "build nonderiv entry list"
    for entry in ndxnlist:
        int_id = str(entry[0]) + str(entry[1]) + str(entry[2]) +\
            'N' + str(entry[22]) + '-' + str(entry[27])
        if int_id not in id_list and str(int(entry[1])) in existingciks:

            is_director = binary_to_boolean(str(entry[4]))
            is_officer = binary_to_boolean(str(entry[5]))
            is_ten_percent = binary_to_boolean(str(entry[6]))
            is_something_else = binary_to_boolean(str(entry[7]))
            issuercik = all_ciks.filter(cik_num=str(int(entry[1])))[0]
            c = entry[28]
            entrytosave =\
                Form345Entry(entry_internal_id=int_id,
                             period_of_report=entry[0],
                             issuer_cik=issuercik,
                             issuer_cik_num=entry[1],
                             reporting_owner_cik_num=entry[2],
                             reporting_owner_name=entry[3],
                             is_director=is_director,
                             is_officer=is_officer,
                             is_ten_percent=is_ten_percent,
                             is_something_else=is_something_else,
                             reporting_owner_title=entry[8],
                             security_title=entry[9],
                             conversion_price=entry[10],
                             transaction_date=entry[11],
                             transaction_code=entry[12],
                             transaction_shares=entry[13],
                             xn_price_per_share=entry[14],
                             xn_acq_disp_code=entry[15],
                             expiration_date=entry[16],
                             underlying_title=entry[17],
                             underlying_shares=entry[18],
                             shares_following_xn=entry[19],
                             direct_or_indirect=entry[20],
                             tenbfive_note=entry[21],
                             transaction_number=entry[22],
                             source_name_partial_path=entry[23],
                             five_not_subject_to_section_sixteen=entry[24],
                             five_form_three_holdings=entry[25],
                             five_form_four_transactions=entry[26],
                             form_type=entry[27],
                             filedatetime=c[:4] + "-" + c[4:6] + "-" + c[6:8] +
                             " " + c[8:10] + ":" + c[10:12] + ":" +
                             c[12:14] + "Z",
                             deriv_or_nonderiv='N'
                             )
            entries.append(entrytosave)
    print 'saving'
    Form345Entry.objects.bulk_create(entries)
    print 'done'
    entries = []
    print "build deriv entry list"
    for entry in dxnlist:
        int_id = str(entry[0]) + str(entry[1]) + str(entry[2]) +\
            'D' + str(entry[22]) + '-' + str(entry[27])
        if int_id not in id_list and str(int(entry[1])) in existingciks:

            is_director = binary_to_boolean(str(entry[4]))
            is_officer = binary_to_boolean(str(entry[5]))
            is_ten_percent = binary_to_boolean(str(entry[6]))
            is_something_else = binary_to_boolean(str(entry[7]))
            issuercik = all_ciks.filter(cik_num=str(int(entry[1])))[0]
            c = entry[28]
            entrytosave =\
                Form345Entry(entry_internal_id=int_id,
                             period_of_report=entry[0],
                             issuer_cik=issuercik,
                             issuer_cik_num=entry[1],
                             reporting_owner_cik_num=entry[2],
                             reporting_owner_name=entry[3],
                             is_director=is_director,
                             is_officer=is_officer,
                             is_ten_percent=is_ten_percent,
                             is_something_else=is_something_else,
                             reporting_owner_title=entry[8],
                             security_title=entry[9],
                             conversion_price=entry[10],
                             transaction_date=entry[11],
                             transaction_code=entry[12],
                             transaction_shares=entry[13],
                             xn_price_per_share=entry[14],
                             xn_acq_disp_code=entry[15],
                             expiration_date=entry[16],
                             underlying_title=entry[17],
                             underlying_shares=entry[18],
                             shares_following_xn=entry[19],
                             direct_or_indirect=entry[20],
                             tenbfive_note=entry[21],
                             transaction_number=entry[22],
                             source_name_partial_path=entry[23],
                             five_not_subject_to_section_sixteen=entry[24],
                             five_form_three_holdings=entry[25],
                             five_form_four_transactions=entry[26],
                             form_type=entry[27],
                             filedatetime=c[:4] + "-" + c[4:6] + "-" + c[6:8] +
                             " " + c[8:10] + ":" + c[10:12] + ":" +
                             c[12:14] + "Z",
                             deriv_or_nonderiv='D'
                             )
            entries.append(entrytosave)
    print 'saving'
    Form345Entry.objects.bulk_create(entries)
    print 'done'
