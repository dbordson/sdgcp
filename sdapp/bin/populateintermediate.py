from sdapp.models import ReportingPerson, Form345Entry,\
    Affiliation, Security, SecurityPriceHist
# from django.db import connection
import datetime
from collections import Counter
from sdapp.bin import updatetitles


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


def link_entries_for_reporting_person_foreign_keys():
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


def link_security_and_security_price_hist(cik, title):
    security_price_hist =\
        SecurityPriceHist.objects.filter(issuer_id=cik)[0]
    ticker = security_price_hist.ticker_sym
    security = \
        Security.objects.get(issuer_id=cik,
                             security_title=title)
    security.ticker = ticker
    security_price_hist.security = security
    security.save()
    security_price_hist.save()


def create_primary_security(cik):
    nonderiv_form_title_set =\
        set(Form345Entry.objects.filter(issuer_cik_num=cik)
            .filter(deriv_or_nonderiv='N')
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
    elif Form345Entry.objects.filter(deriv_or_nonderiv='N')\
            .exclude(short_sec_title__icontains='preferred')\
            .values_list('short_sec_title', flat=True)\
            .count() == 1:
        short_title =\
            Form345Entry.objects.filter(deriv_or_nonderiv='N')\
            .exclude(short_sec_title__icontains='preferred')\
            .values_list('short_sec_title', flat=True)[0]
        link_security_and_security_price_hist(cik, short_title)


# Must create all issuer foreign key linkages in Form345Entry before running

def update_securities():
    print 'Adding new Security objects'
    print '    Sorting...',
    formtitleset =\
        set(Form345Entry.objects
            .values_list('issuer_cik_num', 'short_sec_title'))
    storedtitleset =\
        set(Security.objects
            .values_list('issuer_id', 'security_title'))

    security_titles_to_add =\
        formtitleset\
        - (formtitleset & storedtitleset)
    new_securities = []
    print 'building...',
    for issuer_id, title_to_add in security_titles_to_add:
        rep_form =\
            Form345Entry.objects.filter(short_sec_title=title_to_add)\
            .filter(issuer_cik_num=issuer_id)\
            .order_by('-filedatetime')[0]
        new_security =\
            Security(issuer_id=issuer_id,
                     security_title=title_to_add,
                     ticker=None,
                     deriv_or_nonderiv=rep_form.deriv_or_nonderiv,
                     underlying_title=rep_form.scrubbed_underlying_title)
        new_securities.append(new_security)
    print 'saving...',
    Security.objects.bulk_create(new_securities)
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


updatetitles.update_short_titles()
update_reportingpersons()
update_affiliations()
link_entries_for_reporting_person_foreign_keys()
update_securities()
check_securitypricehist()
