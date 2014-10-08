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
        supersededdt_already_assigned = False
        # The below may happen when a form 5 reflecting an old transaction
        # is filed.
        was_the_filing_superseded_before_filed = \
            entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(security_title=untagged_entry.security_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime__lt=untagged_entry.filedatetime)\
            .filter(transaction_date__gt=untagged_entry.transaction_date)\
            .exists()
        if was_the_filing_superseded_before_filed is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            supersededdt_already_assigned = True

        # The below will happen when a single form provides multiple
        # transactions in a single security.  All transactions but the last
        # will be superseded at the moment the form is filed.

        was_the_filing_superseded_by_the_same_form = \
            entries34\
            .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
            .filter(reporting_owner_cik_num=untagged_entry
                    .reporting_owner_cik_num)\
            .filter(security_title=untagged_entry.security_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(filedatetime=untagged_entry.filedatetime)\
            .filter(transaction_number__gt=untagged_entry.transaction_date)\
            .exists()
        if supersededdt_already_assigned is False and\
                was_the_filing_superseded_by_the_same_form is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            supersededdt_already_assigned = True

        # The below handles the general case where subsequent filings with
        # simultaneous or later transactions supersede current transactions
        #
        # FYI there is voodoo here and in the first if statement, because we
        # don't have a module that is dealing with form amendments in a
        # sophisticated way.  There is the possibility that someone could
        # amend a transaction in the middle of a form 4 but not later
        # transactions.  The logic will supersede the whole day's transactions
        # when it notices a subsequent amendment to a transaction on that day
        # because it doesn't know better (and I can't figure out silver bullet
        # solution, in light of the often inconsistent way these forms are
        # completed).

        if supersededdt_already_assigned is False:
            filtered_entries = entries34\
                .filter(issuer_cik_num=untagged_entry.issuer_cik_num)\
                .filter(reporting_owner_cik_num=untagged_entry
                        .reporting_owner_cik_num)\
                .filter(security_title=untagged_entry.security_title)\
                .filter(expiration_date=untagged_entry.expiration_date)\
                .filter(filedatetime__gt=untagged_entry.filedatetime)\
                .filter(transaction_date__gte=untagged_entry.transaction_date)\
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
