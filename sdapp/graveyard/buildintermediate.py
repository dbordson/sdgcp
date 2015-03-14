from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry,\
    Affiliation, Holding, HoldingType, ClosePrice, SecurityPriceHist,\
    AggHoldingType
# from django.db import connection
import datetime


def weighted_avg(vectorunitoutput, weightingvector):
    dotproduct = sum(p * q for p, q in zip(vectorunitoutput, weightingvector))
    divisor = sum(weightingvector)
    wavg = dotproduct / divisor
    return wavg


def wavgdate(datevector, weightvector):
    try:
        today = datetime.date.today()
        tdvector = [float((entry - today).days) for entry in datevector]
        # the below line doesn't work with single entry lists
        if len(tdvector) == 1:
            return (today + datetime.timedelta(tdvector[0]))
        dotproduct = sum(float(p) * float(q)
                         for p, q in zip(tdvector, weightvector))
        denominator = sum(weightvector)
        wavgdelta = dotproduct / float(denominator)
        wavg = today + datetime.timedelta(wavgdelta)
        return wavg
    except:
        return None


def intrinsicvalcalc(conv_vector, unitsvector, underlyingprice):
    # try:
    up = underlyingprice
    inthemoneyvector = [float(max((up - float(entry)), 0))
                        for entry in conv_vector]
    # the below line doesn't work with single entry lists
    if len(inthemoneyvector) == 1:
        return float(inthemoneyvector[0]) * float(unitsvector[0])
    dotproduct = sum(float(p) * float(q)
                     for p, q in zip(inthemoneyvector, unitsvector))
    return dotproduct
    # except:
        # return None


def update_reportingpersons():
    source_entries = Form345Entry.\
        objects.values_list('reporting_owner_cik_num', flat=True).distinct()
    all_entries = Form345Entry.objects.all()
    # all_issuer_ciks = IssuerCIK.objects.all()
    existing_reportingperson = ReportingPerson.\
        objects.values_list('reporting_owner_cik_num', flat=True).distinct()
    print 'creating reporting person entries'
    entries = []
    print 'building person list'
    for entry in source_entries:
        # try:
        if entry not in existing_reportingperson:
            ciknum = entry
            xns = all_entries.filter(reporting_owner_cik_num=ciknum).\
                exclude(period_of_report__isnull=True).\
                order_by('-period_of_report')
            if xns.exists():
                latest_xn = xns[0]
            else:
                xns = all_entries.filter(reporting_owner_cik_num=ciknum)
                latest_xn = xns[0]
            name = latest_xn.reporting_owner_name
            entrytosave = ReportingPerson(person_name=name,
                                          reporting_owner_cik_num=ciknum)
            entries.append(entrytosave)
            # issuerciks = all_entries.filter(reporting_owner_cik_num=entry).\
                # values_list('issuer_cik_num', flat=True).distinct()
            # for issuercik in issuerciks:
                # entrytosave.issuer = all_issuer_ciks.get(cik_num=issuercik)
        # except:
            # print 'error:', entry
    print 'saving'
    ReportingPerson.objects.bulk_create(entries)
    print 'done updating reporting persons'


def new_affiliation(all_issuer_ciks, issuer_cik, person, name, personentries):
    newaffiliation = Affiliation()
    newaffiliation.issuer = all_issuer_ciks.get(cik_num=str(int(issuer_cik)))
    newaffiliation.reporting_owner = person
    newaffiliation.issuer_cik_num = issuer_cik
    newaffiliation.reporting_owner_cik_num =\
        person.reporting_owner_cik_num
    newaffiliation.person_name = name

    affiliationentries = personentries\
        .filter(issuer_cik_num=issuer_cik)
    if affiliationentries.exclude(period_of_report__isnull=True).exists():
        latestentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('-period_of_report')[0]
        firstentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('period_of_report')[0]
        newaffiliation.first_filing = firstentry.period_of_report
        newaffiliation.most_recent_filing = latestentry\
            .period_of_report
        governingentry = latestentry
        newaffiliation.title = governingentry.reporting_owner_title
        newaffiliation.is_director = governingentry.is_director
        newaffiliation.is_officer = governingentry.is_officer
        newaffiliation.is_ten_percent = governingentry.is_ten_percent
        newaffiliation.is_something_else = governingentry.is_something_else
        return newaffiliation
    # else:
    #     governingentry = affiliationentries[0]
    # newaffiliation.title = governingentry.reporting_owner_title
    # newaffiliation.is_director = governingentry.is_director
    # newaffiliation.is_officer = governingentry.is_officer
    # newaffiliation.is_ten_percent = governingentry.is_ten_percent
    # newaffiliation.is_something_else = governingentry.is_something_else

    return None


def update_affiliation(affiliationupd, all_issuer_ciks, issuer_cik, person,
                       name, personentries):
    affiliationupd.issuer = all_issuer_ciks.get(cik_num=str(int(issuer_cik)))
    affiliationupd.reporting_owner = person
    affiliationupd.person_name = name
    affiliationentries = personentries\
        .filter(issuer_cik_num=issuer_cik)
    if affiliationentries.exclude(period_of_report__isnull=True).exists():
        latestentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('-period_of_report')[0]
        affiliationupd.most_recent_filing = latestentry\
            .period_of_report
        governingentry = latestentry
        affiliationupd.title = governingentry.reporting_owner_title
        affiliationupd.is_director = governingentry.is_director
        affiliationupd.is_officer = governingentry.is_officer
        affiliationupd.is_ten_percent = governingentry.is_ten_percent
        affiliationupd.is_something_else = governingentry.is_something_else
        affiliationupd.save()
    # else:
    #     governingentry = affiliationentries[0]
    # affiliationupd.title = governingentry.reporting_owner_title
    # affiliationupd.is_director = governingentry.is_director
    # affiliationupd.is_officer = governingentry.is_officer
    # affiliationupd.is_ten_percent = governingentry.is_ten_percent
    # affiliationupd.is_something_else = governingentry.is_something_else
    # affiliationupd.save()


def revise_affiliations():
    allpersons = ReportingPerson.objects.all()
    allentries = Form345Entry.objects.all()
    all_issuer_ciks = IssuerCIK.objects.all()
    old_affiliations = Affiliation.objects.all()
    entries = []
    print 'building affiliation list'
    for person in allpersons:
        personentries = allentries\
            .filter(reporting_owner_cik_num=person.reporting_owner_cik_num)
        personissuerciks = personentries\
            .values_list('issuer_cik_num', flat=True).distinct()
        name = person.person_name
        person_cik = person.reporting_owner_cik_num
        for issuer_cik in personissuerciks:
            aff_set = old_affiliations.filter(issuer_cik_num=issuer_cik)\
                .filter(reporting_owner_cik_num=person_cik)
            if not aff_set.exists():
                newaffiliation = new_affiliation(all_issuer_ciks, issuer_cik,
                                                 person, name, personentries)
                if newaffiliation is not None:
                    entries.append(newaffiliation)
            if aff_set.exists():
                # if there is already an entry we determine whether to update
                affiliationentries = personentries\
                    .filter(issuer_cik_num=issuer_cik)\
                    .exclude(period_of_report__isnull=True)
                if affiliationentries.exists():
                    latestentry = affiliationentries\
                        .order_by('-period_of_report')[0]
                    if latestentry.period_of_report !=\
                            aff_set[0].most_recent_filing:
                        update_affiliation(aff_set[0], all_issuer_ciks,
                                           issuer_cik, person, name,
                                           personentries)

    print 'saving'
    Affiliation.objects.bulk_create(entries)
    print 'done updating affiliations'


def new_holding(title, expdate, affiliationentries, affiliation):
    newholding = Holding()
    newholding.issuer = affiliation.issuer
    newholding.owner = affiliation.reporting_owner
    newholding.affiliation = affiliation
    newholding.security_title = title
    newholding.expiration_date = expdate

    holdingentries = affiliationentries.filter(security_title=title)\
        .filter(expiration_date=expdate)
    if holdingentries.exclude(transaction_date__isnull=True).exists():
        latestxndate = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('-transaction_date')[0].transaction_date
        latestxn = holdingentries\
            .filter(transaction_date=latestxndate)\
            .order_by('-transaction_number')[0]
        firstxn = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('transaction_date')[0]
        newholding.first_xn = firstxn.transaction_date
        newholding.most_recent_xn = latestxn.transaction_date
        newholding.units_held = latestxn.shares_following_xn
        newholding.deriv_or_nonderiv = latestxn.deriv_or_nonderiv
        newholding.conversion_price = latestxn.conversion_price
        newholding.underlying_title = latestxn.underlying_title
        newholding.underlying_shares = latestxn.underlying_shares

        return newholding

    # elif len(holdingentries
    #          .exclude(period_of_report__isnull=True)
    #          .order_by('-period_of_report')) != 0:
    #     governingentry = holdingentries\
    #         .exclude(period_of_report__isnull=True)\
    #         .order_by('-period_of_report')[0]
    #     newholding.units_held = governingentry.shares_following_xn
    #     newholding.deriv_or_nonderiv = governingentry.deriv_or_nonderiv
    #     newholding.underlying_title = governingentry.underlying_title
    #     newholding.underlying_shares = governingentry.underlying_shares

    return None


def update_holding(holding, title, expdate, holdingentries, affiliation):
    if holdingentries.exclude(transaction_date__isnull=True).exists():
        latestxndate = holdingentries\
            .exclude(transaction_date__isnull=True)\
            .order_by('-transaction_date')[0].transaction_date
        latestxn = holdingentries\
            .filter(transaction_date=latestxndate)\
            .order_by('-transaction_number')[0]
        holding.most_recent_xn = latestxn\
            .transaction_date
        holding.units_held = latestxn.shares_following_xn
        holding.deriv_or_nonderiv = latestxn.deriv_or_nonderiv
        holding.conversion_price = latestxn.conversion_price
        holding.underlying_title = latestxn.underlying_title
        holding.underlying_shares = latestxn.underlying_shares
        holding.save()

    # elif len(holdingentries
    #          .exclude(period_of_report__isnull=True)
    #          .order_by('-period_of_report')) != 0:
    #     governingentry = holdingentries[0]
    #     holding.units_held = governingentry.shares_following_xn
    #     holding.deriv_or_nonderiv = governingentry.deriv_or_nonderiv
    #     holding.underlying_title = governingentry.underlying_title
    #     holding.underlying_shares = governingentry.underlying_shares


def revise_holdings():
    allentries = Form345Entry.objects.all()
    all_affiliations = Affiliation.objects.all()
    old_holdings = Holding.objects.all()
    entries = []
    print 'building holding list'
    looplength = float(len(all_affiliations))
    count = 0.0
    for affiliation in all_affiliations:
        if float(int(10*count/looplength)) !=\
                float(int(10*(count-1)/looplength)):
            print int(count/looplength*100), 'percent'
        count += 1.0
        # the security title and underlying title mechanic could create issues
        # if someone writes the titles inconsistently from form to form this
        # could be the source of very bad data, so we need to test
        affiliationentries = allentries\
            .filter(issuer_cik_num=
                    affiliation.issuer_cik_num)\
            .filter(reporting_owner_cik_num=
                    affiliation.reporting_owner_cik_num)
        affiliation_security_titles = affiliationentries\
            .values_list('security_title', flat=True).distinct()
        title_expiration_list = []
        # This for loop constructs a flat list of securities with distinct
        # titles AND expiration dates.
        for title in affiliation_security_titles:
            titleexpirationdates = affiliationentries\
                .filter(security_title=title)\
                .values_list('expiration_date', flat=True).distinct()
            if not titleexpirationdates.exists():
                titleset = [title, None]
                title_expiration_list.append(titleset)
            else:
                for expdate in titleexpirationdates:
                    titleset = [title, expdate]
                    title_expiration_list.append(titleset)
        # This for loop determines whether the holding already exists and
        # either adds or updates it as appropriate
        for title_and_date_set in title_expiration_list:
            title, expdate = title_and_date_set
            titledate_holding = old_holdings.filter(security_title=title)\
                .filter(expiration_date=expdate)
            if not titledate_holding.exists():
                newholding = new_holding(title, expdate, affiliationentries,
                                         affiliation)
                if newholding is not None:
                    entries.append(newholding)
            if titledate_holding.exists():
                # if there is already an entry we determine whether to update
                holdingentries = affiliationentries\
                    .filter(security_title=title)\
                    .filter(expiration_date=expdate)
                nonullholdingentries = holdingentries\
                    .exclude(period_of_report__isnull=True)
                if nonullholdingentries.exists():
                    latestentry = nonullholdingentries\
                        .order_by('-period_of_report')[0]
                    if latestentry.transaction_date !=\
                            titledate_holding[0].most_recent_xn:
                        update_holding(titledate_holding[0], title, expdate,
                                       holdingentries, affiliation)
    print 'saving'
    Holding.objects.bulk_create(entries)
    print 'done updating holdings'


def update_entries_for_new_person_foreign_keys():
    all_entries = Form345Entry.objects.all()
    # all_issuer_ciks = IssuerCIK.objects.all()
    existing_reportingperson = ReportingPerson\
        .objects.all()
    print 'adding reporting persons to entries'
    # saveentries = []
    for entry in all_entries:
        if entry.reporting_owner_cik is None:
            reportingowner = existing_reportingperson\
                .get(reporting_owner_cik_num=entry.reporting_owner_cik_num)
            entry.reporting_owner_cik = reportingowner
            entry.save()
    # ReportingPerson.objects.bulk_create(saveentries)
    print 'done updating form345entry reporting person foreign keys'


def new_holdingtype(samp_obj, all_holdings, allentries):
    # tweak below if we need to make sure underlying is distinct)
    holdingsforuse = all_holdings\
        .filter(affiliation=samp_obj.affiliation)\
        .filter(security_title=samp_obj.security_title)\
        .filter(units_held__gte=0)
    entriesforuse = allentries\
        .filter(issuer_cik=samp_obj.issuer)\
        .filter(reporting_owner_cik=samp_obj.owner)
    newholding = HoldingType(issuer=samp_obj.issuer,
                             owner=samp_obj.owner,
                             affiliation=samp_obj.affiliation,
                             security_title=samp_obj.security_title,
                             deriv_or_nonderiv=samp_obj.deriv_or_nonderiv,
                             underlying_title=samp_obj.underlying_title)

    newholding.units_held =\
        sum(holdingsforuse.exclude(units_held=None)
            .values_list('units_held', flat=True))
    # Below finds the underyling value - one possibility for optimization
    # is to do this once for each company, not each holdingtype.
    # one easy way to do this would be to add a latest price field to each
    # issuer CIK, but this means the IssuerCIK model must be updated daily.
    # I don't think this would create a headache, but I'm not sure.
    companycik = samp_obj.issuer
    SecurityPriceHist = SecurityPriceHist.objects.filter(issuer=companycik)
    closeprices = ClosePrice.objects.filter(SecurityPriceHist=SecurityPriceHist)\
        .order_by('-close_date')
    underlyingprice = None
    if len(closeprices) > 0:
        underlyingprice = float(closeprices[0].close_price)

    expirationobj = holdingsforuse.exclude(expiration_date=None)\
        .exclude(units_held=None).exclude(units_held=0)
    expirationlist = expirationobj\
        .values_list('expiration_date', flat=True)
    # Here is where we put in expiration date related fields
    if len(expirationlist) > 0:
        newholding.first_expiration_date = min(expirationlist)
        newholding.last_expiration_date = max(expirationlist)
        sidewaysexpirationandweightlist =\
            [[entry.expiration_date, entry.units_held]
             for entry in expirationobj]
        expdates, unitshelds = zip(*sidewaysexpirationandweightlist)
        newholding.wavg_expiration_date = wavgdate(expdates, unitshelds)
    conversionobj = holdingsforuse.exclude(conversion_price=None)\
        .exclude(units_held=None).exclude(units_held=0)
    conversionpricelist = conversionobj\
        .values_list('conversion_price', flat=True)
    if len(conversionpricelist) > 0:
        newholding.min_conversion_price = min(conversionpricelist)
        newholding.max_conversion_price = max(conversionpricelist)
        sidewaysconversionandunits =\
            [[entry.conversion_price, entry.units_held]
             for entry in conversionobj]
        convprices, unitshelds = zip(*sidewaysconversionandunits)
        newholding.wavg_conversion = weighted_avg(convprices, unitshelds)

    # Here we add underlying price and underlying value
    underlyingsharelist = holdingsforuse.exclude(underlying_shares=None)\
        .values_list('underlying_shares', flat=True)
    if len(underlyingsharelist) > 0:
        newholding.underlying_shares = sum(underlyingsharelist)
    if underlyingprice is not None:

        newholding.underlying_price = underlyingprice
        conversionobj = holdingsforuse.exclude(conversion_price=None)\
            .exclude(underlying_shares=None).exclude(underlying_shares=0)

        conv_prices = conversionobj.values_list('conversion_price',
                                                flat=True)
        if len(conv_prices) > 0:
            sidewaysconvandunitlist =\
                [[entry.conversion_price, entry.underlying_shares]
                 for entry in conversionobj]
            conversionprices, underlyingshares = zip(*sidewaysconvandunitlist)
            newholding.intrinsic_value =\
                intrinsicvalcalc(conversionprices,
                                 underlyingshares,
                                 underlyingprice)
        # If no conversion prices, but it is derivative, treat as excercise
        # price of zero
        elif len(conv_prices) == 0 and samp_obj.deriv_or_nonderiv == 'D'\
                and newholding.underlying_shares is not None:
            newholding.intrinsic_value =\
                float(newholding.underlying_shares) * underlyingprice
        # If no conversion prices and non-derivative, calculate intrinsic
        # value as units times price
        # THIS DOES NOT WORK RIGHT FOR PREFERRED STOCK, TWO CLASSES OF
        # COMMON STOCK; We'll need to fix it.
        elif len(conv_prices) == 0 and samp_obj.deriv_or_nonderiv == 'N'\
                and newholding.units_held is not None:
            newholding.intrinsic_value =\
                float(newholding.units_held) * underlyingprice

    # tweak here if we need to make sure underlying is distinct
    xn_dateobj = entriesforuse.exclude(transaction_date=None)\
        .exclude(transaction_shares=None).exclude(transaction_shares=0)
    xn_dates = xn_dateobj\
        .values_list('transaction_date', flat=True)
    if len(xn_dates) > 0:
        newholding.first_xn = min(xn_dates)
        newholding.most_recent_xn = max(xn_dates)
        sidewaysxndatenandweightlist =\
            [[entry.transaction_date, entry.transaction_shares]
             for entry in xn_dateobj]
        xndates, unitshelds = zip(*sidewaysxndatenandweightlist)
        newholding.wavg_xn_date = wavgdate(xndates, unitshelds)
    newholding.transactions_included = len(entriesforuse)
    newholding.tranches_included = len(holdingsforuse)
    unitstransactedlist = entriesforuse.exclude(transaction_shares=None)\
        .values_list('transaction_shares', flat=True)
    if len(unitstransactedlist) > 0:
        newholding.units_transacted = sum(unitstransactedlist)

    return newholding


def refresh_holdingtypes():
    allentries = Form345Entry.objects.filter(supersededdt=None)
    all_holdings = Holding.objects.exclude(most_recent_xn=None)\
        .exclude(units_held=0)
    all_holdingtypes = HoldingType.objects.exclude(most_recent_xn=None)
    newholdingtypes = []
    print 'building HoldingType list'
    distinctholdtypes = all_holdings.distinct('affiliation', 'security_title')
    looplength = float(len(distinctholdtypes))
    count = 0.0
    for item in distinctholdtypes:
        if float(int(10*count/looplength)) !=\
                float(int(10*(count-1)/looplength)):
            print int(count/looplength*100), 'percent'
        count += 1.0
        itemholdingtypes = all_holdingtypes\
            .filter(affiliation=item.affiliation)\
            .filter(security_title=item.security_title)\
            .filter(units_held__gte=0)
        if len(itemholdingtypes) != 0:
            entriesforuse = allentries\
                .filter(issuer_cik=item.issuer)\
                .filter(reporting_owner_cik=item.owner)\
                .exclude(transaction_date=None)\
                .exclude(transaction_shares=None)\
                .exclude(transaction_shares=0)\
                .order_by('-transaction_date')

            latestentry = entriesforuse[0]
            itemholdingtype = itemholdingtypes[0]
            if itemholdingtype.most_recent_xn != \
                    latestentry.transaction_date:
                newholdingtype = new_holdingtype(item,
                                                 all_holdings,
                                                 allentries)
                newholdingtype.id = itemholdingtype.id
                newholdingtype.save()

        else:
            newholdingtypes.append(new_holdingtype(item,
                                                   all_holdings,
                                                   allentries))
    HoldingType.objects.bulk_create(newholdingtypes)
    print "done"


def new_aggholdingtype(samp_obj, all_holdings, all_holdingtypes, allentries):
    # tweak below if we need to make sure underlying is distinct)
    holdingsforuse = all_holdings\
        .filter(issuer=samp_obj.issuer)\
        .filter(security_title=samp_obj.security_title)\
        .filter(units_held__gte=0)
    holdingtypesforuse = all_holdingtypes\
        .filter(issuer=samp_obj.issuer)\
        .filter(security_title=samp_obj.security_title)
    entriesforuse = allentries\
        .filter(issuer_cik=samp_obj.issuer)
    newholding = AggHoldingType(issuer=samp_obj.issuer,
                                security_title=samp_obj.security_title,
                                deriv_or_nonderiv=samp_obj.deriv_or_nonderiv,
                                underlying_title=samp_obj.underlying_title)

    newholding.units_held =\
        sum(holdingtypesforuse.exclude(units_held=None)
            .values_list('units_held', flat=True))
    # Below finds the underyling value - one possibility for optimization
    # is to do this once for each company, not each holdingtype.
    # one easy way to do this would be to add a latest price field to each
    # issuer CIK, but this means the IssuerCIK model must be updated daily.
    # I don't think this would create a headache, but I'm not sure.
    companycik = samp_obj.issuer
    SecurityPriceHist = SecurityPriceHist.objects.filter(issuer=companycik)
    closeprices = ClosePrice.objects.filter(SecurityPriceHist=SecurityPriceHist)\
        .order_by('-close_date')
    underlyingprice = None
    if len(closeprices) > 0:
        underlyingprice = float(closeprices[0].close_price)

    expirationobj = holdingsforuse.exclude(expiration_date=None)\
        .exclude(units_held=None).exclude(units_held=0)
    expirationlist = expirationobj\
        .values_list('expiration_date', flat=True)
    # Here is where we put in expiration date related fields
    if len(expirationlist) > 0:
        newholding.first_expiration_date = min(expirationlist)
        newholding.last_expiration_date = max(expirationlist)
        sidewaysexpirationandweightlist =\
            [[entry.expiration_date, entry.units_held]
             for entry in expirationobj]
        expdates, unitshelds = zip(*sidewaysexpirationandweightlist)
        newholding.wavg_expiration_date = wavgdate(expdates, unitshelds)
    conversionobj = holdingsforuse.exclude(conversion_price=None)\
        .exclude(units_held=None).exclude(units_held=0)
    conversionpricelist = conversionobj\
        .values_list('conversion_price', flat=True)
    if len(conversionpricelist) > 0:
        newholding.min_conversion_price = min(conversionpricelist)
        newholding.max_conversion_price = max(conversionpricelist)
        sidewaysconversionandunits =\
            [[entry.conversion_price, entry.units_held]
             for entry in conversionobj]
        convprices, unitshelds = zip(*sidewaysconversionandunits)
        newholding.wavg_conversion = weighted_avg(convprices, unitshelds)

    # Here we add underlying price and underlying value
    underlyingsharelist = holdingsforuse.exclude(underlying_shares=None)\
        .values_list('underlying_shares', flat=True)
    if len(underlyingsharelist) > 0:
        newholding.underlying_shares = sum(underlyingsharelist)
    if underlyingprice is not None:

        newholding.underlying_price = underlyingprice
        conversionobj = holdingsforuse.exclude(conversion_price=None)\
            .exclude(underlying_shares=None).exclude(underlying_shares=0)

        conv_prices = conversionobj.values_list('conversion_price',
                                                flat=True)
        if len(conv_prices) > 0:
            sidewaysconvandunitlist =\
                [[entry.conversion_price, entry.underlying_shares]
                 for entry in conversionobj]
            conversionprices, underlyingshares = zip(*sidewaysconvandunitlist)
            newholding.intrinsic_value =\
                intrinsicvalcalc(conversionprices,
                                 underlyingshares,
                                 underlyingprice)
        # If no conversion prices, but it is derivative, treat as excercise
        # price of zero
        elif len(conv_prices) == 0 and samp_obj.deriv_or_nonderiv == 'D'\
                and newholding.underlying_shares is not None:
            newholding.intrinsic_value =\
                float(newholding.underlying_shares) * underlyingprice
        # If no conversion prices and non-derivative, calculate intrinsic
        # value as units times price
        # THIS DOES NOT WORK RIGHT FOR PREFERRED STOCK, TWO CLASSES OF
        # COMMON STOCK; We'll need to fix it.
        elif len(conv_prices) == 0 and samp_obj.deriv_or_nonderiv == 'N'\
                and newholding.units_held is not None:
            newholding.intrinsic_value =\
                float(newholding.units_held) * underlyingprice

    # tweak here if we need to make sure underlying is distinct
    xn_dateobj = entriesforuse.exclude(transaction_date=None)\
        .exclude(transaction_shares=None).exclude(transaction_shares=0)
    xn_dates = xn_dateobj\
        .values_list('transaction_date', flat=True)
    if len(xn_dates) > 0:
        newholding.first_xn = min(xn_dates)
        newholding.most_recent_xn = max(xn_dates)
        sidewaysxndatenandweightlist =\
            [[entry.transaction_date, entry.transaction_shares]
             for entry in xn_dateobj]
        xndates, unitshelds = zip(*sidewaysxndatenandweightlist)
        newholding.wavg_xn_date = wavgdate(xndates, unitshelds)
    newholding.transactions_included = len(entriesforuse)
    newholding.tranches_included = len(holdingsforuse)
    unitstransactedlist = entriesforuse.exclude(transaction_shares=None)\
        .values_list('transaction_shares', flat=True)
    if len(unitstransactedlist) > 0:
        newholding.units_transacted = sum(unitstransactedlist)

    return newholding


def refresh_aggholdingtypes():
    allentries = Form345Entry.objects.exclude(transaction_date=None)
    all_holdings = Holding.objects.exclude(most_recent_xn=None)\
        .exclude(units_held=0)
    all_holdingtypes = HoldingType.objects.exclude(most_recent_xn=None)
    all_aggholdingtypes = AggHoldingType.objects.exclude(most_recent_xn=None)
    newaggholdingtypes = []
    print 'building AggHoldingType list'
    distinctaggholdtypes = all_holdings.distinct('issuer',
                                                 'security_title')
    looplength = float(len(distinctaggholdtypes))
    count = 0.0
    for item in distinctaggholdtypes:
        if float(int(10*count/looplength)) !=\
                float(int(10*(count-1)/looplength)):
            print int(count/looplength*100), 'percent'
        count += 1.0
        itemaggholdingtypes = all_aggholdingtypes\
            .filter(issuer=item.issuer)\
            .filter(security_title=item.security_title)\
            .filter(units_held__gte=0)
        if len(itemaggholdingtypes) != 0:
            entriesforuse = allentries\
                .filter(issuer_cik=item.issuer)\
                .exclude(transaction_date=None)\
                .exclude(transaction_shares=None)\
                .exclude(transaction_shares=0)\
                .order_by('-transaction_date')

            latestentry = entriesforuse[0]
            itemaggholdingtype = itemaggholdingtypes[0]
            if itemaggholdingtype.most_recent_xn != \
                    latestentry.transaction_date:
                newholdingtype = new_aggholdingtype(item,
                                                    all_holdings,
                                                    allentries)
                newholdingtype.id = itemaggholdingtype.id
                newholdingtype.save()

        else:
            newaggholdingtypes.append(new_aggholdingtype(item,
                                                         all_holdings,
                                                         all_holdingtypes,
                                                         allentries))
    AggHoldingType.objects.bulk_create(newaggholdingtypes)
    print "done"


# update_reportingpersons()
# revise_affiliations()
# revise_holdings()
# update_entries_for_new_person_foreign_keys()
refresh_holdingtypes()
refresh_aggholdingtypes()