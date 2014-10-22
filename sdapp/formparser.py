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


# class e:
#     entry_internal_id = None
#     period_of_report = None
#     issuer_cik = None
#     issuer_cik_num = None
#     reporting_owner_cik = None
#     reporting_owner_cik_num = None
#     reporting_owner_name = None
#     is_director = None
#     is_officer = None
#     is_ten_percent = None
#     is_something_else = None
#     reporting_owner_title = None
#     security_title = None
#     conversion_price = None
#     transaction_date = None
#     transaction_code = None
#     transaction_shares = None
#     xn_price_per_share = None
#     xn_acq_disp_code = None
#     expiration_date = None
#     underlying_title = None
#     underlying_shares = None
#     shares_following_xn = None
#     direct_or_indirect = None
#     tenbfive_note = None
#     transaction_number = None
#     source_name_partial_path = None
#     five_not_subject_to_section_sixteen = None
#     five_form_three_holdings = None
#     five_form_four_transactions = None
#     form_type = None
#     deriv_or_nonderiv = None
#     filedatetime = None
#     supersededdt = None


def filemapper(CIK):
    xmldirectory = []
    filedir = os.path.expanduser('~/AutomatedFTP/storage' + str(CIK) + '/')
    alreadyparsedfilenames =\
        set(Form345Entry.objects.values_list('source_name_partial_path',
                                             flat=True))
    for root, dirs, files in os.walk(filedir):
        for fileentry in files:
            if fileentry.endswith('.xml') and\
                    fileentry not in alreadyparsedfilenames:
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


def parse(root, child, child2, entrynumber, deriv_or_nonderiv, xmlfilename,
          tenbfivenotenames):
    a = Form345Entry()

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
    # MAKE SURE THIS WORKS
    # Sees if any 10b5-1 footnotes are on the list
    for fnotereturn in child2.iter('footnoteId'):
        fnotenumber = fnotereturn.get('id')
        if fnotenumber in tenbfivenotenames:
            a.tenbfive_note = 1

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

    a.entry_internal_id =\
        str(a.filedatetime)\
        + str(a.issuer_cik_num)\
        + str(a.reporting_owner_cik_num)\
        + deriv_or_nonderiv\
        + str(entrynumber)\
        + '-'\
        + str(a.form_type)

    return a


def formcrawl(xmlfilename):
    tree = ET.parse(xmlfilename)
    root = tree.getroot()

    # Finds the 10b5-1 footnotes
    tenbfivenotenames = []
    for fnotes in root.findall('footnotes'):
        for fnote in fnotes.findall('footnote'):
            if '10b5-1' in fnote.text:
                tenbfivenotenames.append(fnote.get('id'))

    formentries = []
    NonDerivEntryNumber = 1

    for child in root.findall('nonDerivativeTable'):
        deriv_or_nonderiv = 'N'
        for child2 in child.findall("./"):
            entry = parse(root, child, child2, NonDerivEntryNumber,
                          deriv_or_nonderiv, xmlfilename,
                          tenbfivenotenames)
            formentries.append(entry)
            NonDerivEntryNumber += 1

    DerivEntryNumber = 1
    for child in root.findall('derivativeTable'):
        deriv_or_nonderiv = 'D'
        for child2 in child.findall('./'):
            entry = parse(root, child, child2, DerivEntryNumber,
                          deriv_or_nonderiv, xmlfilename,
                          tenbfivenotenames)
            formentries.append(entry)
            DerivEntryNumber += 1

    return formentries


def formentryinsert():
    entries = []
    parseerrorlist = []
    totaldirectorylength = 0
    i = 0
    for CIKentry in IssuerCIK.objects.values_list('cik_num', flat=True):
        print 'Scanning CIK: ', CIKentry, '...'
        entries = []
        xmlfiledirectory = filemapper(CIKentry)
        totaldirectorylength += len(xmlfiledirectory)

        for xmlfile in xmlfiledirectory:
            try:
                entries += formcrawl(xmlfile)
                i += 1
            except:
                parseerrorlist.append(xmlfile)
        print 'Saving...',
        Form345Entry.objects.bulk_create(entries)
        print 'Done with CIK.'
    # meanlist = []
    # for item in ndxnlist:
    #     meanlist.append(item[13])
    # if meanlist[0] is None:
    #     meanlist = [0]
    # print float(sum(meanlist))
    # print len(meanlist)
    # print "average", float(sum(meanlist)) / len(meanlist)

    print "The total number of files reviewed was:", totaldirectorylength
    print "how many times did the for loop run?", i

    # print ndxnlist[1][2]
    print "Length of error list indicating omitted files:", len(parseerrorlist)
    print "Here are any files from above that were filed in 2005 or later:"
    oldyears = ['94', '95', '96', '97', '98', '99',
                '00', '01', '02', '03', '04']
    for line in parseerrorlist:
        if not any(line.find('-' + oldyear + '-') != -1
                   for oldyear in oldyears):
            print line

    print 'Done adding new entries'
