from sdapp.models import Form345Entry, FullForm
import os
import sys
from decimal import Decimal

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


def convert_string_to_datetimestring(c):
    return c[:4] + "-" + c[4:6] + "-" + c[6:8] + " " + c[8:10] + ":" +\
        c[10:12] + ":" + c[12:14] + "Z"


def scrub_title(security_title_string):
    if security_title_string is None:
        return None

#     # Below looks for put options -- we wouldn't want to scrub these out
#     # because it would be very important to identify them, if they exist.
#     short_circuit_phrase_list = [
#         'right to sell',
#         'put option',
#     ]
#     scrubbed_str = security_title_string.lower()

#     for phrase in short_circuit_phrase_list:
#         if scrubbed_str.find(phrase) != -1:
#             return scrubbed_str

#     # Below strips surplus phrases from the front of the title.
#     strip_beginning_phrase_dict = {
#         '198': 4,
#         '199': 4,
#         '200': 4,
#         '201': 4,
#         '202': 4,
#     }

#     for phrase in strip_beginning_phrase_dict:
#         if scrubbed_str.find(phrase) != -1\
#                 and scrubbed_str.find(phrase) < 5:
#             scrubbed_str = \
#                 scrubbed_str[scrubbed_str.find(phrase) +
#                              strip_beginning_phrase_dict[phrase]:]
#     scrubbed_str = scrubbed_str.strip(' .,;:')

#     # Below strips surplus phrases from the end of the title.
    strip_end_phrase_list = [
        'par value',
        'Par Value',
        '198',
        '199',
        '200',
        '201',
        '202',
    ]

    for phrase in strip_end_phrase_list:
        if security_title_string.find(phrase) > 9:
            security_title_string = \
                security_title_string[:security_title_string.find(phrase)]

    replace_phrase_dict = {
        'optiion': 'option',
        'Optiion': 'option',
        'corporation': 'corp',
        'Corporation': 'Corp',
        'compensation': 'comp',
        'Compensation': 'Comp',
        'incorporated': 'inc',
        'Incorporated': 'Inc',
        'plan dividend': 'plan',
        'Plan Dividend': 'Plan'
    }

    for error in replace_phrase_dict:
        if error in security_title_string:
            security_title_string =\
                security_title_string\
                .replace(error, replace_phrase_dict[error])
    security_title_string = security_title_string.strip(' .,;:')
    return security_title_string


# Extracts text attribute
def t_att(numchar, treeobject, path):
    try:
        a = treeobject.find(path).text[0:numchar]
    except:
        a = None

    return a


# Extracts float attribute
def f_att(numdec, treeobject, path):
    try:
        a = round(float(treeobject.find(path).text), numdec)
    except:
        a = None

    return a


# Extracts boolean attribute
def b_att(treeobject, path):
    try:
        if treeobject.find(path).text[0:1] == '1':
            a = True
        else:
            a = False
    except:
        a = False

    return a


# def path_to_filename(xmlfilename):
# This function finds the last '/' in the string to extract the filename.
# The first line is kind of voodoo, but it uses slice notation to take
# whole string, but backwards -- this is used because python has no find
# from the right function.
#     last_slash_position = xmlfilename[::-1].find('/')
#     return xmlfilename[len(xmlfilename) - last_slash_position:]


def parse(root, child, child2, entrynumber, deriv_or_nonderiv, xmlfilepath,
          tenbfivenotenames, filingdatetimestring):
    a = Form345Entry()

    a.period_of_report = t_att(20, root, 'periodOfReport')
    a.issuer_cik_num = int(t_att(10, root, 'issuer/issuerCik'))
    a.issuer_name = t_att(80, root, 'issuer/issuerName')
    a.issuer_cik_id = a.issuer_cik_num
    # a.reporting_owner_cik = SPACER
    a.reporting_owner_cik_num =\
        int(t_att(10, root, 'reportingOwner/reportingOwnerId/rptOwnerCik'))
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
    a.security_title = scrub_title(t_att(80, child2, 'securityTitle/value'))
    # a.short_sec_title = scrub_title(a.security_title)
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
        scrub_title(t_att(80,
                          child2,
                          'underlyingSecurity/underlyingSecurityTitle/value'))
    # a.scrubbed_underlying_title = scrub_title(a.underlying_title)
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
    a.sec_path = xmlfilepath
    a.five_not_subject_to_section_sixteen =\
        t_att(15, root, 'notSubjectToSection16')
    a.five_form_three_holdings = t_att(15, root, 'form3HoldingsReported')
    a.five_form_four_transactions =\
        t_att(15, root, 'form4TransactionsReported')
    a.form_type = \
        t_att(5, root,
              'documentType')
    a.deriv_or_nonderiv = deriv_or_nonderiv
    a.filedatetime =\
        convert_string_to_datetimestring(filingdatetimestring)
    a.supersededdt = None

    a.entry_internal_id =\
        str(a.filedatetime) + '-'\
        + str(a.issuer_cik_num) + '-'\
        + str(a.reporting_owner_cik_num) + '-'\
        + deriv_or_nonderiv + '-'\
        + str(entrynumber) + '-'\
        + str(a.form_type)

    if deriv_or_nonderiv == 'D' and a.conversion_price is None:
        a.conversion_price = Decimal(0.0)

    if a.transaction_date is None and\
            a.transaction_code is None and\
            a.shares_following_xn is None and\
            a.transaction_shares is not None:
        a.shares_following_xn = a.transaction_shares
        a.transaction_shares = None
    if a.shares_following_xn is None:
        a.shares_following_xn = Decimal(0.0)

    return a


def filingdatetimepull(textstring):
    try:
        tag = '<ACCEPTANCE-DATETIME>'
        snippetstart = textstring.find(tag)
        snippet = textstring[snippetstart + len(tag):
                             snippetstart + len(tag) + 14]
        return snippet
    except:
        return "error!"


def formcrawl(fullformobject):
    textstring = fullformobject.text
    xmlfilepath = fullformobject.sec_path

    # Pulls xml out of the full form text
    filingdatetimestring = filingdatetimepull(textstring)
    startxml = textstring.find('<XML>') + 5
    endxml = textstring.find('</XML>')
    xmlstring = textstring[startxml:endxml].strip('\n')

    # Parses XML
    root = ET.fromstring(xmlstring)

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
                          deriv_or_nonderiv, xmlfilepath,
                          tenbfivenotenames, filingdatetimestring)
            formentries.append(entry)
            NonDerivEntryNumber += 1

    DerivEntryNumber = 1
    for child in root.findall('derivativeTable'):
        deriv_or_nonderiv = 'D'
        for child2 in child.findall('./'):
            entry = parse(root, child, child2, DerivEntryNumber,
                          deriv_or_nonderiv, xmlfilepath,
                          tenbfivenotenames, filingdatetimestring)
            formentries.append(entry)
            DerivEntryNumber += 1

    return formentries


def formentryinsert():

    storedformpathset =\
        set(FullForm.objects.values_list('sec_path', flat=True))
    parsedformpathset =\
        set(Form345Entry.objects.values_list('sec_path', flat=True))

    # The below compares the above sets to find what forms are stored but
    # not parsed.
    paths_to_parse =\
        storedformpathset - (storedformpathset & parsedformpathset)

    forms_to_parse =\
        FullForm.objects.filter(pk__in=list(paths_to_parse))

    entries = []
    parseerrorlist = []
    i = 0
    totalformslength = len(paths_to_parse)
    count = 0.0
    print 'Beginning parse loop'
    for form in forms_to_parse:
        try:
            entries += formcrawl(form)
            i += 1
        except:
            parseerrorlist.append(form)

        # The below reports if 10% progress has been made.
        if float(int(10*count/totalformslength)) !=\
                float(int(10*(count-1)/totalformslength)):
            print int(count/totalformslength*100), 'percent'
        count += 1.0

        # This saves is 1 mb of entires have been parsed
        if sys.getsizeof(entries) > 1000000:  # 1 mb
            print 'Saving'
            Form345Entry.objects.bulk_create(entries)
            entries = []
            print 'Done with this batch, starting next batch'

    # This saves the remaining entries not saved above
    print 'Saving'
    Form345Entry.objects.bulk_create(entries)

    print "The total number of files reviewed was:", totalformslength
    print "how many times did the for loop run?", i
    print "Length of error list indicating omitted files:", len(parseerrorlist)
    print "Here are any files from above that were filed in 2005 or later:"
    oldyears = ['94', '95', '96', '97', '98', '99',
                '00', '01', '02', '03', '04']
    for line in parseerrorlist:
        if not any(line.sec_path.find('-' + oldyear + '-') != -1
                   for oldyear in oldyears):
            print line.sec_path

    print 'Done adding new entries'

formentryinsert()
