
import os
# This code will work best if the stored files are in a subdirectory of
# the current working directory.
cwd = os.getcwd()
lencwd = len(cwd)

# This is a new function in this version. textattribute() handles attribute
# exceptions, which we need when a tag is missing (e.g. there is no value in
# the expiration date of an option tranche.  I don't try to analyze here and
# just note errors)


def textattribute(function):
    try:
        a = function.text
    except AttributeError:
        a = None

    return a


def floattextattribute(function):
    try:
        a = round(float(function.text), 4)
    except AttributeError:
        a = None

    return a

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def xn4parse(xmlfilename):
    #Below pulls the tree as an object
    tree = ET.parse(xmlfilename)
    #Below pulls the root element of the parsed string
    root = tree.getroot()
    # The root object has child nodes
    # below nested loops iterate to find the non-derivative and then
    # derivative transactions ("NonDerivXns"). First it defines the list then
    # it constructs each transaction in order then it adds them to the list

    # One open question is: what about the footnotes? should we try to pull
    # those in now or wait until later? So first, make an empty list (which
    # will be a list of transaction data lists, that is a 2d list)
    NonDerivXns = []
    #10b5-1 note detector (in the whole Form 4)
    footnotenames = []
    for fnotes in root.findall('footnotes'):
        for fnote in fnotes.findall('footnote'):
            if '10b5-1' in fnote.text:
                footnotenames.append(fnote.get('id'))
    NonDerivXnNumber = 1
    #Now iterate over each non-deriv transaction
    for child in root.findall('nonDerivativeTable'):
        #print "Found a child"

    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('nonDerivativeTransaction'):
            #print "Found a grandchild"
            NonDerivXn = ['err', 'err', 'err', 'err', 'err',
                          'err', 'err', 'err', 'err', 'err',
                          None,  'err', 'err', 'err', 'err',
                          'err', None,  None,  None,  'err',
                          'err',    0,  'err', 'err', None,
                          None,  None,    '4', 'err']
            NonDerivXn[0] = textattribute(root.find('periodOfReport'))
            NonDerivXn[1] = textattribute(root.find('issuer/issuerCik'))
            NonDerivXn[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            NonDerivXn[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            NonDerivXn[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            NonDerivXn[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            NonDerivXn[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            NonDerivXn[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            NonDerivXn[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            NonDerivXn[9] = textattribute(child2.find('securityTitle/value'))
            #placeholder
            NonDerivXn[11] = textattribute(child2.find(
                'transactionDate/value'))
            NonDerivXn[12] = textattribute(child2.find(
                'transactionCoding/transactionCode'))
            NonDerivXn[13] = floattextattribute(child2.find(
                'transactionAmounts/transactionShares/value'))
            NonDerivXn[14] = floattextattribute(child2.find(
                'transactionAmounts/transactionPricePerShare/value'))
            NonDerivXn[15] = textattribute(child2.find(
                'transactionAmounts/transactionAcquiredDisposedCode/value'))
            #placeholder
            #placeholder
            #placeholder
            NonDerivXn[19] = floattextattribute(child2.find(
                'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
            )
            NonDerivXn[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if NonDerivXn[4] is None:
                NonDerivXn[4] = '0'
            if NonDerivXn[5] is None:
                NonDerivXn[5] = '0'
            if NonDerivXn[6] is None:
                NonDerivXn[6] = '0'
            if NonDerivXn[7] is None:
                NonDerivXn[7] = '0'

            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if NonDerivXn[8] == 'AttributeError' and NonDerivXn[5] == str(0):
                NonDerivXn[8] = None

            #10b5-1 transaction finder

            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    NonDerivXn[21] = 1
            NonDerivXn[22] = NonDerivXnNumber
            NonDerivXn[23] = xmlfilename[lencwd:]
            NonDerivXn[27] = textattribute(root.find('documentType'))
            NonDerivXn[28] = textattribute(root.find('dateandtime'))
            NonDerivXnNumber += 1
            #print NonDerivXn
            NonDerivXns.append(NonDerivXn)

    DerivXns = []
    DerivXnNumber = 1
    #Now iterate over each deriv transaction
    for child in root.findall('derivativeTable'):
    #   print "Found a child"

    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('derivativeTransaction'):
    #       print "Found a grandchild"
            DerivXn = ['err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err',    0,  'err', 'err', None,
                       None,  None,    '4', 'err']
            DerivXn[0] = textattribute(root.find('periodOfReport'))
            DerivXn[1] = textattribute(root.find('issuer/issuerCik'))
            DerivXn[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            DerivXn[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            DerivXn[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            DerivXn[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            DerivXn[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            DerivXn[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            DerivXn[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            DerivXn[9] = textattribute(child2.find('securityTitle/value'))
            DerivXn[10] = textattribute(child2.find(
                'conversionOrExercisePrice/value'))
            DerivXn[11] = textattribute(child2.find('transactionDate/value'))
            DerivXn[12] = textattribute(child2.find(
                'transactionCoding/transactionCode'))
            DerivXn[13] = floattextattribute(child2.find(
                'transactionAmounts/transactionShares/value'))
            DerivXn[14] = floattextattribute(child2.find(
                'transactionAmounts/transactionPricePerShare/value'))
            DerivXn[15] = textattribute(child2.find(
                'transactionAmounts/transactionAcquiredDisposedCode/value'))
            DerivXn[16] = textattribute(child2.find(
                'expirationDate/value'))
            DerivXn[17] = textattribute(child2.find(
                'underlyingSecurity/underlyingSecurityTitle/value'))
            DerivXn[18] = floattextattribute(child2.find(
                'underlyingSecurity/underlyingSecurityShares/value'))
            DerivXn[19] = floattextattribute(child2.find(
                'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
            )
            DerivXn[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if DerivXn[4] is None:
                DerivXn[4] = '0'
            if DerivXn[5] is None:
                DerivXn[5] = '0'
            if DerivXn[6] is None:
                DerivXn[6] = '0'
            if DerivXn[7] is None:
                DerivXn[7] = '0'

            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if DerivXn[8] == 'AttributeError' and DerivXn[5] == str(0):
                DerivXn[8] = None

            # Handles errors when no conversion or price per share is
            # provided (e.g. for RSUs that convert 1:1)
            if DerivXn[10] == 'AttributeError':
                DerivXn[10] = None

            if DerivXn[13] == 'AttributeError':
                DerivXn[13] = None

            if DerivXn[14] == 'AttributeError':
                DerivXn[14] = None

            # Handles errors when no expiration date is provided (e.g. for
            # phantom stock units that don't expire)
            if DerivXn[16] == 'AttributeError':
                DerivXn[16] = None

            #10b5-1 transaction finder
            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    DerivXn[21] = 1
            DerivXn[22] = DerivXnNumber
            DerivXn[23] = xmlfilename[lencwd:]
            DerivXn[27] = textattribute(root.find('documentType'))
            DerivXn[28] = textattribute(root.find('dateandtime'))
            DerivXnNumber += 1
            #print DerivXn
            DerivXns.append(DerivXn)

    #print "done with the function"
#This returns the two 2d lists as a tuple (so that we don't have to go
# back and figure out which transactions were deriv/nonderiv)
    #print NonDerivXns, DerivXns
    return NonDerivXns, DerivXns


def xn5parse(xmlfilename):
    # The below line pulls in the element tree functions in python and renames
    # it ET. Below pulls the tree as an object (I think)
    tree = ET.parse(xmlfilename)
    # Below pulls the root element of the parsed string
    root = tree.getroot()
    # The root object has child nodes
    # below nested loops iterate to find the non-derivative and then derivative
    # transactions ("NonDerivXns")
    # First it defines the list then it constructs each transaction in order
    # then it adds them to the list
    NonDerivXns = []
    #10b5-1 note detector (in the whole Form 4)
    footnotenames = []
    for fnotes in root.findall('footnotes'):
        for fnote in fnotes.findall('footnote'):
            if '10b5-1' in fnote.text:
                footnotenames.append(fnote.get('id'))
    NonDerivXnNumber = 1
    #Now iterate over each non-deriv transaction
    for child in root.findall('nonDerivativeTable'):
    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('nonDerivativeTransaction'):
            #print "Found a grandchild"
            NonDerivXn = ['err', 'err', 'err', 'err', 'err',
                          'err', 'err', 'err', 'err', 'err',
                          None,  'err', 'err', 'err', 'err',
                          'err', None,  None,  None,  'err',
                          'err',    0,  'err', 'err', 'err',
                          'err', 'err',   '5', 'err']
            NonDerivXn[0] = textattribute(root.find('periodOfReport'))
            NonDerivXn[1] = textattribute(root.find('issuer/issuerCik'))
            NonDerivXn[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            NonDerivXn[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            NonDerivXn[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            NonDerivXn[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            NonDerivXn[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            NonDerivXn[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            NonDerivXn[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            NonDerivXn[9] = textattribute(child2.find('securityTitle/value'))
            #placeholder
            NonDerivXn[11] = textattribute(child2.find(
                'transactionDate/value'))
            NonDerivXn[12] = textattribute(child2.find(
                'transactionCoding/transactionCode'))
            NonDerivXn[13] = floattextattribute(child2.find(
                'transactionAmounts/transactionShares/value'))
            NonDerivXn[14] = floattextattribute(child2.find(
                'transactionAmounts/transactionPricePerShare/value'))
            NonDerivXn[15] = textattribute(child2.find(
                'transactionAmounts/transactionAcquiredDisposedCode/value'))
            #placeholder
            #placeholder
            #placeholder
            NonDerivXn[19] = floattextattribute(child2.find(
                'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
            )
            NonDerivXn[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if NonDerivXn[4] is None:
                NonDerivXn[4] = '0'
            if NonDerivXn[5] is None:
                NonDerivXn[5] = '0'
            if NonDerivXn[6] is None:
                NonDerivXn[6] = '0'
            if NonDerivXn[7] is None:
                NonDerivXn[7] = '0'

            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if NonDerivXn[8] == 'AttributeError' and NonDerivXn[5] == str(0):
                NonDerivXn[8] = None

            #10b5-1 transaction finder

            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    NonDerivXn[21] = 1
            NonDerivXn[22] = NonDerivXnNumber
            NonDerivXn[23] = xmlfilename[lencwd:]
            #These are solely related to Form 5
            NonDerivXn[24] = textattribute(root.find('notSubjectToSection16'))
            NonDerivXn[25] = textattribute(root.find('form3HoldingsReported'))
            NonDerivXn[26] = textattribute(root.find(
                'form4TransactionsReported'))
            NonDerivXn[28] = textattribute(root.find('dateandtime'))
            NonDerivXnNumber += 1
            #print NonDerivXn
            NonDerivXns.append(NonDerivXn)

    DerivXns = []
    DerivXnNumber = 1
    #Now iterate over each deriv transaction
    for child in root.findall('derivativeTable'):
    #   print "Found a child"

    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('derivativeTransaction'):
    #       print "Found a grandchild"
            DerivXn = ['err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err', 'err', 'err', 'err', 'err',
                       'err',    0,  'err', 'err', 'err'
                       'err', 'err',   '5', 'err']
            DerivXn[0] = textattribute(root.find('periodOfReport'))
            DerivXn[1] = textattribute(root.find('issuer/issuerCik'))
            DerivXn[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            DerivXn[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            DerivXn[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            DerivXn[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            DerivXn[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            DerivXn[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            DerivXn[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            DerivXn[9] = textattribute(child2.find('securityTitle/value'))
            DerivXn[10] = textattribute(child2.find(
                'conversionOrExercisePrice/value'))
            DerivXn[11] = textattribute(child2.find('transactionDate/value'))
            DerivXn[12] = textattribute(child2.find(
                'transactionCoding/transactionCode'))
            DerivXn[13] = floattextattribute(child2.find(
                'transactionAmounts/transactionShares/value'))
            DerivXn[14] = floattextattribute(child2.find(
                'transactionAmounts/transactionPricePerShare/value'))
            DerivXn[15] = textattribute(child2.find(
                'transactionAmounts/transactionAcquiredDisposedCode/value'))
            DerivXn[16] = textattribute(child2.find('expirationDate/value'))
            DerivXn[17] = textattribute(child2.find(
                'underlyingSecurity/underlyingSecurityTitle/value'))
            DerivXn[18] = floattextattribute(child2.find(
                'underlyingSecurity/underlyingSecurityShares/value'))
            DerivXn[19] = floattextattribute(child2.find(
                'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
            )
            DerivXn[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if DerivXn[4] is None:
                DerivXn[4] = '0'
            if DerivXn[5] is None:
                DerivXn[5] = '0'
            if DerivXn[6] is None:
                DerivXn[6] = '0'
            if DerivXn[7] is None:
                DerivXn[7] = '0'

            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if DerivXn[8] == 'AttributeError' and DerivXn[5] == str(0):
                DerivXn[8] = None

            # Handles errors when no conversion or price per share is
            # provided (e.g. for RSUs that convert 1:1)
            if DerivXn[10] == 'AttributeError':
                DerivXn[10] = None

            if DerivXn[13] == 'AttributeError':
                DerivXn[13] = None

            if DerivXn[14] == 'AttributeError':
                DerivXn[14] = None

            # Handles errors when no expiration date is provided (e.g. for
            # phantom stock units that don't expire)
            if DerivXn[16] == 'AttributeError':
                DerivXn[16] = None

            #10b5-1 transaction finder
            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    DerivXn[21] = 1
            DerivXn[22] = DerivXnNumber
            DerivXn[23] = xmlfilename[lencwd:]
            #These are solely related to Form 5
            DerivXn[24] = textattribute(root.find('notSubjectToSection16'))
            DerivXn[25] = textattribute(root.find('form3HoldingsReported'))
            DerivXn[26] = textattribute(root.find(
                'form4TransactionsReported'))
            DerivXn[28] = textattribute(root.find('dateandtime'))
            DerivXnNumber += 1
            #print DerivXn
            DerivXns.append(DerivXn)

    #print "done with the function"
#This returns the two 2d lists as a tuple (so that we don't have to go
# back and figure out which transactions were deriv/nonderiv)
    #print NonDerivXns, DerivXns
    return NonDerivXns, DerivXns


def xn3parse(xmlfilename):
    # Note:
    # The below line pulls in the element tree functions in python and renames
    # it ET
    #Below pulls the tree as an object (I think)
    tree = ET.parse(xmlfilename)
    #Below pulls the root element of the parsed string
    root = tree.getroot()
    #The root object has child nodes
    # below nested loops iterate to find the non-derivative and then derivative
    # transactions ("NonDerivHs"). First it defines the list then it constructs
    # each transaction in order then it adds them to the list

    # One open question is: what about the footnotes? should we try to pull
    # those in now or wait until later?
    # So first, make an empty list (which will be a list of transaction data
    # lists, that is a 2d list)
    NonDerivHs = []
    #10b5-1 note detector (in the whole Form 4)
    footnotenames = []
    # For form 3, 10b5-1 should never pop up; I left it in, because if it does,
    # there may be a file handling problem.
    for fnotes in root.findall('footnotes'):
        for fnote in fnotes.findall('footnote'):
            if '10b5-1' in fnote.text:
                footnotenames.append(fnote.get('id'))
    NonDerivHNumber = 1
    #Now iterate over each non-deriv transaction
    for child in root.findall('nonDerivativeTable'):
        #print "Found a child"

    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('nonDerivativeHolding'):
            #print "Found a grandchild"
            NonDerivH = ['err', 'err', 'err', 'err', 'err',
                         'err', 'err', 'err', 'err', 'err',
                         None,  None,  None,  None,  None,
                         None,  None,  None,  None,  'err',
                         'err',    0,  'err', 'err', None,
                         None,  None,    '3', 'err']
            NonDerivH[0] = textattribute(root.find('periodOfReport'))
            NonDerivH[1] = textattribute(root.find('issuer/issuerCik'))
            NonDerivH[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            NonDerivH[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            NonDerivH[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            NonDerivH[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            NonDerivH[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            NonDerivH[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            NonDerivH[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            NonDerivH[9] = textattribute(child2.find('securityTitle/value'))
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            NonDerivH[19] = floattextattribute(child2.find(
                'postTransactionAmounts/sharesOwnedFollowingTransaction/value')
            )
            NonDerivH[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if NonDerivH[4] is None:
                NonDerivH[4] = '0'
            if NonDerivH[5] is None:
                NonDerivH[5] = '0'
            if NonDerivH[6] is None:
                NonDerivH[6] = '0'
            if NonDerivH[7] is None:
                NonDerivH[7] = '0'
            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if NonDerivH[8] == 'AttributeError' and NonDerivH[5] == str(0):
                NonDerivH[8] = 'N/A'

            #10b5-1 transaction finder

            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    NonDerivH[21] = 1
            if NonDerivH[21] == 1:
                NonDerivH[21] = 'Error, unexpected 10b5-1 entry'

            NonDerivH[22] = NonDerivHNumber
            NonDerivH[23] = xmlfilename[lencwd:]
            NonDerivH[28] = textattribute(root.find('dateandtime'))
            NonDerivHNumber += 1
            #print NonDerivH
            NonDerivHs.append(NonDerivH)

    DerivHs = []
    DerivHNumber = 1
    #Now iterate over each deriv transaction
    for child in root.findall('derivativeTable'):
    #   print "Found a child"

    #This finds each transaction, making a list of its attributes
        for child2 in child.findall('derivativeHolding'):
    #       print "Found a grandchild"
            DerivH = ['err', 'err', 'err', 'err', 'err',
                      'err', 'err', 'err', 'err', 'err',
                      'err', None,  None,  None,  None,
                      None,  'err', 'err', 'err', None,
                      'err',    0,  'err', 'err', None,
                      None,  None,    '3', 'err']
            DerivH[0] = textattribute(root.find('periodOfReport'))
            DerivH[1] = textattribute(root.find('issuer/issuerCik'))
            DerivH[2] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerCik'))
            DerivH[3] = textattribute(root.find(
                'reportingOwner/reportingOwnerId/rptOwnerName'))
            DerivH[4] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isDirector'))
            DerivH[5] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOfficer'))
            DerivH[6] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isTenPercentOwner'))
            DerivH[7] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/isOther'))
            DerivH[8] = textattribute(root.find(
                'reportingOwner/reportingOwnerRelationship/officerTitle'))
            DerivH[9] = textattribute(child2.find('securityTitle/value'))
            DerivH[10] = textattribute(child2.find(
                'conversionOrExercisePrice/value'))
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            # placeholder
            DerivH[16] = textattribute(child2.find(
                'expirationDate/value'))
            DerivH[17] = textattribute(child2.find(
                'underlyingSecurity/underlyingSecurityTitle/value'))
            DerivH[18] = floattextattribute(child2.find(
                'underlyingSecurity/underlyingSecurityShares/value'))
            # placeholder
            DerivH[20] = textattribute(child2.find(
                'ownershipNature/directOrIndirectOwnership/value'))

            # For the type of filer (officer, director, etc.) sometimes a
            # negative response is 0 and sometimes it is an omission. The below
            # code conforms these conventions.
            if DerivH[4] is None:
                DerivH[4] = '0'
            if DerivH[5] is None:
                DerivH[5] = '0'
            if DerivH[6] is None:
                DerivH[6] = '0'
            if DerivH[7] is None:
                DerivH[7] = '0'
            # Handles errors due to blank officer title entry for non-officer
            # filers (e.g. directors).
            if DerivH[8] == 'AttributeError' and DerivH[5] == str(0):
                DerivH[8] = None
            if DerivH[10] == 'AttributeError':
                DerivH[10] = None

            # Handles errors when no expiration date is provided (e.g. for
            # phantom stock units that don't expire)
            if DerivH[16] == 'AttributeError':
                DerivH[16] = 'Not in form'

            #10b5-1 transaction finder
            for fnotereturn in child2.iter('footnoteId'):
                fnotenumber = fnotereturn.get('id')
                for fnotenumber in footnotenames:
                    DerivH[21] = 1
            DerivH[22] = DerivHNumber
            DerivH[23] = xmlfilename[lencwd:]
            DerivH[28] = textattribute(root.find('dateandtime'))
            DerivHNumber += 1
            #print DerivH
            DerivHs.append(DerivH)

    #print "done with the function"
#This returns the two 2d lists as a tuple (so that we don't have to go
# back and figure out which transactions were deriv/nonderiv)
    #print NonDerivHs, DerivHs
    return NonDerivHs, DerivHs


def formtestandparse(xmlfilename):
    results = ([], [])
    #Below pulls the tree as an object (I think)
    tree = ET.parse(xmlfilename)
    #Below pulls the root element of the parsed string
    root = tree.getroot()
    if textattribute(root.find('documentType')) == '4' or \
       textattribute(root.find('documentType')) == '4/A':
        results = xn4parse(xmlfilename)

    if textattribute(root.find('documentType')) == '5':
        results = xn5parse(xmlfilename)

    if textattribute(root.find('documentType')) == '3':
        results = xn3parse(xmlfilename)

    return results
