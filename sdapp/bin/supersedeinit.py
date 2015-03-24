from sdapp.models import Form345Entry
# from django.db import connection
import datetime
from decimal import Decimal


def convert_date_to_datetimestring(date):
    c = str(date)
    return c[:10] + " 23:59:59Z"

# entries34, untagged_entries


def string_date_with_years_added(yearsafter, date_in_iso):
    c = date_in_iso
    return str(int(c[0:4]) + yearsafter) + c[4:10] + " " + c[11:19] + "Z"


def superseded_initialize():
    print "Calculating superseded dates of unsuperseded forms..."
    entries34 = Form345Entry.objects\
        .exclude(filedatetime=None)\
        .exclude(short_sec_title=None)
    untagged_entry_ids =\
        entries34.filter(supersededdt=None).values_list('pk', flat=True)
    looplength = float(len(untagged_entry_ids))
    counter = 0.0
    today = datetime.date.today()
    nonofficercutoffyears = 5
    nonofficercutoffdate = datetime.date(today.year-nonofficercutoffyears,
                                         today.month, today.day)
    nonofficercutoffdt = convert_date_to_datetimestring(nonofficercutoffdate)
    officercutoffyears = 2
    officercutoffdate = datetime.date(today.year-officercutoffyears,
                                      today.month, today.day)
    officercutoffdt = convert_date_to_datetimestring(officercutoffdate)
    for untagged_entry_id in untagged_entry_ids:
        untagged_entry = Form345Entry.objects\
            .get(pk=untagged_entry_id)
        # Counter below
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print int(counter/looplength*100), 'percent'
        counter += 1.0
        # Logic below
        supersededdt_already_assigned = False

        # This adjusts Form 3, 3/A entries to work, since they lack
        # transaction dates and instead tie to the period of the report.
        date_of_untagged_entry = untagged_entry.transaction_date
        direct_or_indirect = untagged_entry.direct_or_indirect
        if date_of_untagged_entry is None:
            date_of_untagged_entry = \
                untagged_entry.filedatetime.date()

        # The below may happen when a form 5 reflecting an old transaction
        # is filed.
        was_the_filing_superseded_before_filed = \
            entries34\
            .filter(issuer_cik=untagged_entry.issuer_cik)\
            .filter(reporting_owner_cik=untagged_entry
                    .reporting_owner_cik)\
            .filter(short_sec_title=untagged_entry.short_sec_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(scrubbed_underlying_title=untagged_entry
                    .scrubbed_underlying_title)\
            .filter(filedatetime__lt=untagged_entry.filedatetime)\
            .filter(transaction_date__gt=date_of_untagged_entry)\
            .filter(direct_or_indirect=direct_or_indirect)\
            .exists()
        if was_the_filing_superseded_before_filed is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below will happen when a single form provides multiple
        # transactions in a single security.  All transactions but the last
        # will be superseded at the moment the form is filed.

        was_the_filing_superseded_by_the_same_form = \
            entries34\
            .filter(issuer_cik=untagged_entry.issuer_cik)\
            .filter(reporting_owner_cik=untagged_entry
                    .reporting_owner_cik)\
            .filter(short_sec_title=untagged_entry.short_sec_title)\
            .filter(expiration_date=untagged_entry.expiration_date)\
            .filter(scrubbed_underlying_title=
                    untagged_entry.scrubbed_underlying_title)\
            .filter(filedatetime=untagged_entry.filedatetime)\
            .filter(transaction_number__gt=untagged_entry.transaction_number)\
            .filter(direct_or_indirect=direct_or_indirect)\
            .exists()
        if supersededdt_already_assigned is False and\
                was_the_filing_superseded_by_the_same_form is True:
            untagged_entry.supersededdt = untagged_entry.filedatetime
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below handles derivatives that have expired

        if supersededdt_already_assigned is False and\
                untagged_entry.expiration_date is not None and\
                today >= untagged_entry.expiration_date:
            untagged_entry.supersededdt = \
                convert_date_to_datetimestring(untagged_entry.expiration_date)
            untagged_entry.save()
            supersededdt_already_assigned = True

        # The below handles transactions that close out a position (leave the
        # reporting person with zero shares remaining.  We don't want to use
        # these positions as current holdings, as it makes logical sense to
        # say that a position of zero shares is superseded, leaving the person
        # with no position in the security.
        if supersededdt_already_assigned is False and\
                untagged_entry.shares_following_xn == Decimal('0'):
            untagged_entry.supersededdt = untagged_entry.filedatetime
            untagged_entry.save()
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
                .filter(issuer_cik=untagged_entry.issuer_cik)\
                .filter(reporting_owner_cik=untagged_entry
                        .reporting_owner_cik)\
                .filter(short_sec_title=untagged_entry.short_sec_title)\
                .filter(expiration_date=untagged_entry.expiration_date)\
                .filter(scrubbed_underlying_title=
                        untagged_entry.scrubbed_underlying_title)\
                .filter(filedatetime__gt=untagged_entry.filedatetime)\
                .filter(direct_or_indirect=direct_or_indirect)\
                .exclude(transaction_date__lte=date_of_untagged_entry)\
                .order_by('filedatetime')
            if filtered_entries.exists():
                untagged_entry.supersededdt = filtered_entries[0].filedatetime
                untagged_entry.save()
                supersededdt_already_assigned = True

        # Does the filer (if an officer) have any recent activity?
        are_there_recent_trades_for_the_officer = \
            entries34\
            .filter(issuer_cik=untagged_entry.issuer_cik)\
            .filter(reporting_owner_cik=untagged_entry
                    .reporting_owner_cik)\
            .filter(filedatetime__gt=officercutoffdt).exists()
        if supersededdt_already_assigned is False and\
                untagged_entry.is_officer is True and\
                are_there_recent_trades_for_the_officer is False:
            latest_file_dt_as_iso = \
                entries34\
                .filter(issuer_cik=untagged_entry.issuer_cik)\
                .filter(reporting_owner_cik=untagged_entry
                        .reporting_owner_cik)\
                .latest('filedatetime').filedatetime.isoformat()
            supersededdt_for_filer = \
                string_date_with_years_added(officercutoffyears,
                                             latest_file_dt_as_iso)
            untagged_entry.supersededdt = supersededdt_for_filer
            untagged_entry.save()
            supersededdt_already_assigned = True

        are_there_recent_trades_for_the_nonofficer = \
            entries34\
            .filter(issuer_cik=untagged_entry.issuer_cik)\
            .filter(reporting_owner_cik=untagged_entry
                    .reporting_owner_cik)\
            .filter(filedatetime__gt=nonofficercutoffdt).exists()
        if supersededdt_already_assigned is False and\
                untagged_entry.is_officer is False and\
                are_there_recent_trades_for_the_nonofficer is False:
            latest_file_dt_as_iso = \
                entries34\
                .filter(issuer_cik=untagged_entry.issuer_cik)\
                .filter(reporting_owner_cik=untagged_entry
                        .reporting_owner_cik)\
                .latest('filedatetime').filedatetime.isoformat()
            supersededdt_for_filer = \
                string_date_with_years_added(nonofficercutoffyears,
                                             latest_file_dt_as_iso)
            untagged_entry.supersededdt = supersededdt_for_filer
            untagged_entry.save()

            supersededdt_already_assigned = True
    print 'Done.'
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
