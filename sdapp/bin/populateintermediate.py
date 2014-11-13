from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry,\
    Affiliation, ClosePrice, SecurityPriceHist
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
    unicode_reporting_owner_ciks =\
        Form345Entry.objects\
        .values_list('reporting_owner_cik_num', flat=True).distinct()
    form_reporting_owner_cik_set =\
        set([int(a) for a in unicode_reporting_owner_ciks])

    unicode_existing_reporting_person_cik_set =\
        set(ReportingPerson.objects
            .values_list('reporting_owner_cik_num', flat=True).distinct())
    existing_reporting_person_cik_set =\
        set([int(a) for a in unicode_existing_reporting_person_cik_set])

    reporting_person_ciks_to_add =\
        form_reporting_owner_cik_set\
        - (form_reporting_owner_cik_set & existing_reporting_person_cik_set)

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

    print 'saving'
    ReportingPerson.objects.bulk_create(new_persons)
    print 'done updating reporting persons'


# check lineup of int type primary keys against storage in Form345Entry model
# The tell should be runaway record creation each time the script is run.
def add_affiliations():
    unicode_combinations = \
        Affiliation.objects\
        .values_list('issuer_id', 'reporting_owner_id')
    storedaffiliations =\
        set([(int(a), int(b)) for a, b in unicode_combinations])

    unicode_combinations =\
        Form345Entry.objects\
        .values_list('issuer_cik_num', 'reporting_owner_cik_num')
    reporting_person_issuer_combinations =\
        set([(int(a), int(b)) for a, b in unicode_combinations])

    affiliations_cik_combinations_to_add =\
        reporting_person_issuer_combinations\
        - (reporting_person_issuer_combinations & storedaffiliations)

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
    Affiliation.objects.bulk_create(new_affiliations)

update_reportingpersons()
add_affiliations()
