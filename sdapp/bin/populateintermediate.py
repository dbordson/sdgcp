from sdapp.models import (ReportingPerson, Form345Entry,
                          Affiliation, Security, SecurityPriceHist)
# from django.db import connection
import datetime
from collections import Counter
from sdapp.bin import updatetitles


def weighted_avg(vectorunitoutput, weightingvector):
    dotproduct = sum(p * q for p, q in zip(vectorunitoutput, weightingvector))
    divisor = sum(weightingvector)
    wavg = dotproduct / divisor
    return wavg


def median(medlist):
    medlist.sort()
    i = len(medlist)/2
    if len(medlist) % 2 == 0:
        median_number = (medlist[i] + medlist[i-1])/2
    else:
        median_number = medlist[i]
    return median_number


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
    up = underlyingprice
    inthemoneyvector = [float(max((up - float(entry)), 0))
                        for entry in conv_vector]
    if len(inthemoneyvector) == 1:
        return float(inthemoneyvector[0]) * float(unitsvector[0])
    else:
        dotproduct =\
            sum(float(p) * float(q)
                for p, q in zip(inthemoneyvector, unitsvector))
        return dotproduct


def update_reportingpersons():
    print 'Adding new ReportingPerson objects...'
    print '    Sorting...',
    form_reporting_owner_cik_set =\
        set(Form345Entry.objects
            .values_list('reporting_owner_cik_num', flat=True))

    existing_reporting_person_cik_set =\
        set(ReportingPerson.objects
            .values_list('reporting_owner_cik_num', flat=True).distinct())

    reporting_person_ciks_to_add =\
        form_reporting_owner_cik_set\
        - (form_reporting_owner_cik_set & existing_reporting_person_cik_set)

    print 'building...',
    new_persons = []
    for reporting_person_cik_to_add in reporting_person_ciks_to_add:
        cik = reporting_person_cik_to_add
        name =\
            Form345Entry.objects.filter(reporting_owner_cik_num=cik)\
            .order_by('-filedatetime')[0].reporting_owner_name
        # Figure out how to update name of person if it changes?
        persontosave =\
            ReportingPerson(person_name=name,
                            reporting_owner_cik_num=cik)
        new_persons.append(persontosave)

    print 'saving...',
    ReportingPerson.objects.bulk_create(new_persons)
    print 'done.'


# check lineup of int type primary keys against storage in Form345Entry model
# The tell should be runaway record creation each time the script is run.
def update_affiliations():
    print 'Adding new Affiliation objects...'
    print '    Sorting...',
    storedaffiliations = \
        set(Affiliation.objects
            .values_list('issuer_id', 'reporting_owner_id'))
    # storedaffiliations =\
        # set([(int(a), int(b)) for a, b in unicode_combinations])

    reporting_person_issuer_combinations =\
        set(Form345Entry.objects
            .values_list('issuer_cik_num', 'reporting_owner_cik_num'))

    affiliations_cik_combinations_to_add =\
        reporting_person_issuer_combinations\
        - (reporting_person_issuer_combinations & storedaffiliations)

    print 'building...',
    new_affiliations = []
    for cik_combination in affiliations_cik_combinations_to_add:
        issuer_cik_num = cik_combination[0]
        reporting_owner_cik_num = cik_combination[1]
        latest_entry =\
            Form345Entry.objects\
            .filter(issuer_cik_num=issuer_cik_num)\
            .filter(reporting_owner_cik_num=reporting_owner_cik_num)\
            .order_by('-filedatetime')[0]

        new_affiliation =\
            Affiliation(issuer_id=issuer_cik_num,
                        reporting_owner_id=reporting_owner_cik_num,
                        person_name=latest_entry.reporting_owner_name)
        new_affiliations.append(new_affiliation)
    print 'saving...',
    Affiliation.objects.bulk_create(new_affiliations)
    print 'done.'


def link_entries_for_reporting_person_and_affiliation_foreign_keys():
    print 'Linking Form345Entry objects to ReportingPerson objects...'
    print '    Sorting...',
    reporting_owner_ciks_with_unlinked_forms =\
        Form345Entry.objects.filter(reporting_owner_cik=None)\
        .values_list('reporting_owner_cik_num', flat=True).distinct()
    print 'linking and saving...',
    for reporting_owner_cik in reporting_owner_ciks_with_unlinked_forms:
        reporting_owner =\
            ReportingPerson.objects\
            .get(reporting_owner_cik_num=reporting_owner_cik)
        Form345Entry.objects.filter(reporting_owner_cik=None)\
            .filter(reporting_owner_cik_num=reporting_owner_cik)\
            .update(reporting_owner_cik=reporting_owner)
    print 'done.'

    print 'Linking Form345Entry objects to Affiliation objects...'
    print '    Sorting...',
    affiliations_with_unlinked_forms =\
        Form345Entry.objects.filter(affiliation=None)\
        .values_list('reporting_owner_cik', 'issuer_cik').distinct()
    print 'linking and saving...',
    for reporting_owner_cik, issuer_cik\
            in affiliations_with_unlinked_forms:
        # print reporting_owner_cik, issuer_cik_num
        affiliation =\
            Affiliation.objects\
            .filter(issuer_id=issuer_cik)\
            .get(reporting_owner_id=reporting_owner_cik)
        # print affiliation, affiliation.id
        Form345Entry.objects.filter(reporting_owner_cik=reporting_owner_cik)\
            .filter(reporting_owner_cik=reporting_owner_cik)\
            .filter(issuer_cik=issuer_cik)\
            .update(affiliation=affiliation.id)
    print 'done.'


def link_security_and_security_price_hist(cik, title):
    security_price_hist =\
        SecurityPriceHist.objects.filter(issuer_id=cik)[0]
    ticker = security_price_hist.ticker_sym
    security = \
        Security.objects.get(issuer_id=cik,
                             short_sec_title=title)
    security.ticker = ticker
    security_price_hist.security = security
    security.save()
    security_price_hist.save()


def create_primary_security(cik):
    nonderiv_form_title_set =\
        set(Form345Entry.objects.filter(issuer_cik_num=cik)
            .exclude(deriv_or_nonderiv='D')
            .values_list('short_sec_title', flat=True))

    deriv_form_underlying_title_list =\
        Form345Entry.objects.filter(issuer_cik_num=cik)\
        .filter(deriv_or_nonderiv='D')\
        .exclude(scrubbed_underlying_title=None)\
        .values_list('scrubbed_underlying_title', flat=True)

    # Below says that the publicly traded stock is probably the one that most
    # compensatory derivative are convertible into.
    if len(deriv_form_underlying_title_list) != 0:
        underlying_short_title = Counter(deriv_form_underlying_title_list)
        primary_nonderiv_title = underlying_short_title.most_common(1)[0][0]
        if primary_nonderiv_title in nonderiv_form_title_set:
            link_security_and_security_price_hist(cik, primary_nonderiv_title)

    # If the above does not give a result (perhaps because only stock grants),
    # then the below checks to see if there is just one non_derivative title,
    # in which case, that's probably the public stock.
    elif Form345Entry.objects.exclude(deriv_or_nonderiv='D')\
            .exclude(short_sec_title__icontains='preferred')\
            .values_list('short_sec_title', flat=True)\
            .count() == 1:
        short_title =\
            Form345Entry.objects.exclude(deriv_or_nonderiv='D')\
            .exclude(short_sec_title__icontains='preferred')\
            .values_list('short_sec_title', flat=True)[0]
        link_security_and_security_price_hist(cik, short_title)


# Must create all issuer foreign key linkages in Form345Entry before running
# MUST FIX TO DISTINGUISH BETWEEN SECURITIES WITH SAME NAME BUT DIFFERENT
# UNDERLYING SECURITIES (already put in basic mechanics, check flow through to
# rest of script and other scripts)
def update_securities():
    print 'Completing or adding complete Security objects...'
    print '    Sorting...',
    formtitleset =\
        set(Form345Entry.objects
            .values_list('issuer_cik_num',
                         'short_sec_title',
                         'scrubbed_underlying_title',
                         'deriv_or_nonderiv'))
    storedtitleset =\
        set(Security.objects
            .values_list('issuer_id',
                         'short_sec_title',
                         'scrubbed_underlying_title',
                         'deriv_or_nonderiv'))

    security_titles_to_add =\
        formtitleset\
        - (formtitleset & storedtitleset)
    new_securities = []
    print 'building...',
    # Adjust to permit new securities to be filled in without underlying
    # and later filled in.  This logic could create a problem if a security
    # with a single short title is actually two separate securities which are
    # referenced only as underlying securities.  I suspect this risk is remote.
    for issuer_id, title_to_add, underlying_title, deriv_or_nonderiv\
            in security_titles_to_add:
        short_title_with_no_underlying = \
            Security.objects.filter(short_sec_title=title_to_add)\
            .filter(scrubbed_underlying_title=None)\
            .filter(deriv_or_nonderiv=None)\
            .filter(issuer_id=issuer_id)
        if short_title_with_no_underlying.exists():
            sec_for_update = short_title_with_no_underlying[0]
            sec_for_update.scrubbed_underlying_title = underlying_title
            sec_for_update.deriv_or_nonderiv = deriv_or_nonderiv
            sec_for_update.save()
        else:
            new_security =\
                Security(issuer_id=issuer_id,
                         short_sec_title=title_to_add,
                         ticker=None,
                         deriv_or_nonderiv=deriv_or_nonderiv,
                         scrubbed_underlying_title=underlying_title)
            new_securities.append(new_security)
    print 'saving...',
    Security.objects.bulk_create(new_securities)
    print 'done.'
    # Below adds securities which are only named as underlying securities
    # and not directly transacted in the available form history.  For example
    # this could happen if a company goes public and insiders hold only deriv.
    # securities (RSUs and common stock) and do not directly hold common stock.
    print 'Adding incomplete Security objects...'
    print '    Sorting...',
    incomplete_formtitleset =\
        set(Form345Entry.objects
            .exclude(scrubbed_underlying_title=None)
            .values_list('issuer_cik_num',
                         'scrubbed_underlying_title'))
    incomplete_storedtitleset =\
        set(Security.objects
            .values_list('issuer_id',
                         'short_sec_title'))
    incomplete_security_titles_to_add =\
        incomplete_formtitleset\
        - (incomplete_formtitleset & incomplete_storedtitleset)
    new_incomplete_securities = []
    print 'building...',
    for issuer_id, title_to_add in incomplete_security_titles_to_add:
        new_incomplete_security =\
            Security(issuer_id=issuer_id,
                     short_sec_title=title_to_add,
                     ticker=None,
                     deriv_or_nonderiv=None,
                     scrubbed_underlying_title=None)
        new_incomplete_securities.append(new_incomplete_security)
    print 'saving...',
    Security.objects.bulk_create(new_incomplete_securities)
    print 'done.'

    # below determines if any don't have at least one associated
    # ticker.
    print 'Finding and linking objects with associated',
    print 'SecurityPriceHist objects, none of which are linked to a ',
    print 'security...'
    print '    Sorting...',
    issuer_ciks_with_linked_tickers =\
        set(Security.objects.exclude(ticker=None)
            .values_list('issuer', flat=True))

    issuer_ciks_tickers =\
        set(SecurityPriceHist.objects.values_list('issuer', flat=True))

    ciks_with_all_tickers_unlinked =\
        issuer_ciks_tickers\
        - (issuer_ciks_tickers & issuer_ciks_with_linked_tickers)

    print 'linking and saving...',
    for cik in ciks_with_all_tickers_unlinked:
        create_primary_security(cik)
    print 'done.'


def link_form_objects_to_securities():
    print 'Finding and linking Form345Entry objects with Security objects'
    print '    Sorting, linking and saving...',
    unlinked_form_objects =\
        Form345Entry.objects.filter(security=None)\
        .values_list('issuer_cik_num', 'short_sec_title').distinct()
    for issuer_cik_num, short_sec_title in unlinked_form_objects:
        security =\
            Security.objects.get(issuer_id=issuer_cik_num,
                                 short_sec_title=short_sec_title)
        Form345Entry.objects.filter(security=None)\
            .filter(issuer_cik_num=issuer_cik_num)\
            .filter(short_sec_title=short_sec_title)\
            .update(security=security)
    print 'done.'


def check_securitypricehist():
    print 'Checking for unlinked tickers...',
    unlinked_security_price_hist =\
        SecurityPriceHist.objects.filter(security=None)\
        .values_list('ticker_sym', 'issuer')
    if len(unlinked_security_price_hist) != 0:
        print ''
        print 'LOOK OUT--THE FOLLOWING SecurityPriceHist OBJECTS ARE UNLINKED'
        print unlinked_security_price_hist
        print 'YOU SHOULD FIX THIS!'
    else:
        print 'none found.'


def link_underlying_securities():
    print 'Checking for unlinked Form345Entry objects...'

    unlinked_form_ciks_and_underlying_set =\
        set(Form345Entry.objects.filter(deriv_or_nonderiv='D')
            .filter(underlying_security=None)
            .exclude(scrubbed_underlying_title=None)
            .values_list('issuer_cik', 'scrubbed_underlying_title')
            .distinct())
    underlying_securities =\
        set(Security.objects.filter(deriv_or_nonderiv='N')
            .exclude(short_sec_title=None)
            .values_list('issuer', 'short_sec_title'))
    print '    Sorting...',
    underlying_securities_to_link =\
        unlinked_form_ciks_and_underlying_set &\
        underlying_securities

    underlying_securities_to_link_list = list(underlying_securities_to_link)

    print 'linking and saving...',
    for cik, underlying_title in underlying_securities_to_link_list:
        security_id = \
            Security.objects.filter(issuer=cik)\
            .filter(short_sec_title=underlying_title)[0].id
        Form345Entry.objects.filter(deriv_or_nonderiv='D')\
            .filter(issuer_cik=cik)\
            .filter(underlying_security=None)\
            .filter(scrubbed_underlying_title=underlying_title)\
            .update(underlying_security=security_id)
    print 'done.'


def populate_conversion_factors():
    print 'Replacing conversion factors...'
    latest_conv_list = Form345Entry.objects.filter(transaction_code='M')\
        .filter(deriv_or_nonderiv='D')\
        .exclude(underlying_security__ticker=None)\
        .values_list('security_id', flat=True).distinct()
    for security_id in latest_conv_list:
        sampleentries =\
            Form345Entry.objects.filter(security=security_id)\
            .filter(transaction_code='M')\
            .order_by('filedatetime')[:10]\
            .values_list('underlying_shares', 'transaction_shares')
        conversion_multiples = [p / q for p, q in sampleentries]
        conversion_multiple = median(conversion_multiples)
        Security.objects.filter(id=security_id)\
            .update(conversion_multiple=conversion_multiple)
    print 'done.'


updatetitles.update_short_titles()
update_reportingpersons()
update_affiliations()
link_entries_for_reporting_person_and_affiliation_foreign_keys()
update_securities()
link_form_objects_to_securities()
check_securitypricehist()
link_underlying_securities()
populate_conversion_factors()