from sdapp.models import Form345Entry
# from django.db import connection
# import datetime


# all_entries, untagged_entries

def superseded_initialize():
    all_entries = Form345Entry.objects\
        .exclude(transaction_date=None)
    untagged_entries = all_entries.filter(supersededdt=None)
    looplength = float(len(untagged_entries))
    counter = 0.0
    for untagged_entry in untagged_entries:
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print int(counter/looplength*100), 'percent'
        counter += 1.0
        # print "%s of %s" % (counter, looplength)
        filtered_entries = all_entries\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(security_title=untagged_entry.security_title)\
            .filter(filedatetime__gt=untagged_entry.filedatetime)\
            .order_by('filedatetime')
        if filtered_entries.exists():
            untagged_entry.supersededdt = filtered_entries[0].filedatetime
            untagged_entry.save()
    return

# How do you best remove the entries recently tagged as superseded from the
# query set?

superseded_initialize()
