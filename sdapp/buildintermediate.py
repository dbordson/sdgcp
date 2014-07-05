from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry, Affiliation


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
            if len(xns) > 0:
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
    if affiliationentries.exclude(period_of_report__isnull=True) != []:
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
    else:
        governingentry = affiliationentries[0]
    newaffiliation.title = governingentry.reporting_owner_title
    newaffiliation.is_director = governingentry.is_director
    newaffiliation.is_officer = governingentry.is_officer
    newaffiliation.is_ten_percent = governingentry.is_ten_percent
    newaffiliation.is_something_else = governingentry.is_something_else

    return newaffiliation


def update_affiliation(affiliationupd, all_issuer_ciks, issuer_cik, person,
                       name, personentries):
    affiliationupd.issuer = all_issuer_ciks.get(cik_num=str(int(issuer_cik)))
    affiliationupd.reporting_owner = person
    affiliationupd.person_name = name
    affiliationentries = personentries\
        .filter(issuer_cik_num=issuer_cik)
    if affiliationentries.exclude(period_of_report__isnull=True) != []:
        latestentry = affiliationentries\
            .exclude(period_of_report__isnull=True)\
            .order_by('-period_of_report')[0]
        affiliationupd.most_recent_filing = latestentry\
            .period_of_report
        governingentry = latestentry
    else:
        governingentry = affiliationentries[0]
    affiliationupd.title = governingentry.reporting_owner_title
    affiliationupd.is_director = governingentry.is_director
    affiliationupd.is_officer = governingentry.is_officer
    affiliationupd.is_ten_percent = governingentry.is_ten_percent
    affiliationupd.is_something_else = governingentry.is_something_else
    affiliationupd.save()


def revise_affiliations():
    allpersons = ReportingPerson.objects.all()
    allentries = Form345Entry.objects.all()
    all_issuer_ciks = IssuerCIK.objects.all()
    old_affiliations = Affiliation.objects.all()
    entries = []
    # add mechanic to add if the affiliation is new and
    # update if the affiliation is not new
    # update if latests transaction period of affiliation
    # is not equal to the transaction period for the latest
    # Form345Entry
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
            if len(aff_set) == 0:
                newaffiliation = new_affiliation(all_issuer_ciks, issuer_cik,
                                                 person, name, personentries)
                entries.append(newaffiliation)
            if len(aff_set) != 0:
                # if there is already an entry we determine whether to update
                affiliationentries = personentries\
                    .filter(issuer_cik_num=issuer_cik)
                if len(affiliationentries
                        .exclude(period_of_report__isnull=True)) != 0:
                    latestentry = affiliationentries\
                        .exclude(period_of_report__isnull=True)\
                        .order_by('-period_of_report')[0]
                    if latestentry.period_of_report !=\
                            aff_set[0].most_recent_filing:
                        update_affiliation(aff_set[0], all_issuer_ciks,
                                           issuer_cik, person, name,
                                           personentries)

    print 'saving'
    Affiliation.objects.bulk_create(entries)
    print 'done updating affiliations'


update_reportingpersons()
revise_affiliations()
