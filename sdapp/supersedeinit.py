from sdapp.models import Form345Entry
# from django.db import connection
# import datetime


# entries34, untagged_entries

def superseded_initialize():
    entries34 = Form345Entry.objects\
        .exclude(filedatetime=None)\
        .exclude(form_type="5")\
        .exclude(form_type="5/A")
    untagged_entries = entries34.filter(supersededdt=None)
    looplength = float(len(untagged_entries))
    counter = 0.0
    for untagged_entry in untagged_entries:
        # Counter below
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print int(counter/looplength*100), 'percent'
        counter += 1.0
        # Logic below
        supersededdt_assigned = False
        was_the_filing_superseded_when_filed = \
            filtered_entries = entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(security_title=untagged_entry.security_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime__lt=untagged_entry.filedatetime)\
            .filter(transaction_date__gt=untagged_entry.transaction_date)\
            .exists()
        if was_the_filing_superseded_when_filed is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            supersededdt_assigned = True
        
        if 

        filtered_entries = entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(security_title=untagged_entry.security_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime__gt=untagged_entry.filedatetime)\
            .order_by('filedatetime')
        if filtered_entries.exists():
            untagged_entry.supersededdt = filtered_entries[0].filedatetime
            untagged_entry.save()
    return

# not just transactions
# first check if same datetime filed
# if same datetime test for xn number, if not same,
# test for closest date
# treat form 5 correctly? -- maybe use xn date as a proxy for filedate,
# because would be a poor assumption to assume it is latest?

# How do you best remove the entries recently tagged as superseded from the
# query set?

superseded_initialize()
