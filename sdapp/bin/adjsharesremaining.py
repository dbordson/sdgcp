from sdapp.models import Form345Entry
from django.db.models import Sum

# Intro note: the way shares following transaction variable is defined is
# confusing.  The logic tracks rolls forms forward by filing date and not by
# transaction date.  The reason for this is to avoid retroactively informing
# the adjusted shares with information about transactions that preceded the
# transaction in question but which were filed afterward.

# Also this logic ignores amended forms because it would be quite hard to
# to incorporate amendments.


def transaction_share_calculator(shares_acquired_disposed):
    form_transaction_shares = 0
    if shares_acquired_disposed.exists():
        for xn_acq_disp_code, transaction_shares\
                in shares_acquired_disposed:
            if xn_acq_disp_code == 'A':
                form_transaction_shares += transaction_shares
            if xn_acq_disp_code == 'D':
                form_transaction_shares -= transaction_shares
    return form_transaction_shares

affiliations_and_securities_with_unadjusted_indirect_entries = \
    Form345Entry.objects.filter(shares_following_xn_is_adjusted=False)\
    .filter(direct_or_indirect='I')\
    .exclude(form_type='3/A')\
    .exclude(form_type='4/A')\
    .exclude(form_type='5/A')\
    .values_list('affiliation',
                 'short_sec_title',
                 'scrubbed_underlying_title',
                 'expiration_date')\
    .distinct()


for affiliation, short_sec_title, scrubbed_underlying_title,\
        expiration_date in \
        affiliations_and_securities_with_unadjusted_indirect_entries:

    sec_paths_with_unadjusted_indirect_entries = \
        Form345Entry.objects.filter(shares_following_xn_is_adjusted=False)\
        .filter(affiliation=affiliation)\
        .filter(expiration_date=expiration_date)\
        .filter(direct_or_indirect='I')\
        .filter(short_sec_title=short_sec_title)\
        .filter(scrubbed_underlying_title=scrubbed_underlying_title)\
        .exclude(form_type='3/A')\
        .exclude(form_type='4/A')\
        .exclude(form_type='5/A')\
        .order_by('filedatetime')\
        .values_list('sec_path')\
        .distinct()
    # The "type" is unadjusted forms that represent the same bucket of security
    entries_of_this_type =\
        Form345Entry.objects.filter(shares_following_xn_is_adjusted=False)\
        .filter(affiliation=affiliation)\
        .filter(expiration_date=expiration_date)\
        .filter(direct_or_indirect='I')\
        .filter(short_sec_title=short_sec_title)\
        .filter(scrubbed_underlying_title=scrubbed_underlying_title)\
        .exclude(form_type='3/A')\
        .exclude(form_type='4/A')\
        .exclude(form_type='5/A')\
        .order_by('filedatetime')

    adjusted_entries_of_this_type =\
        Form345Entry.objects.filter(shares_following_xn_is_adjusted=True)\
        .filter(affiliation=affiliation)\
        .filter(expiration_date=expiration_date)\
        .filter(direct_or_indirect='I')\
        .filter(short_sec_title=short_sec_title)\
        .filter(scrubbed_underlying_title=scrubbed_underlying_title)\
        .order_by('-filedatetime')

    # This logic finds the last adjusted entry to get the starting shares
    # remaining value.  This only works if the last entry adjusted was filed
    # before all unadjusted entries.  This should be true based on how this 
    # script works, but be careful to update the below if this changes.
    if adjusted_entries_of_this_type.exists():
        starting_shares =\
            adjusted_entries_of_this_type[0].shares_following_xn_is_adjusted
    else:
        starting_shares = 0

    shares_held = starting_shares

    for sec_path in sec_paths_with_unadjusted_indirect_entries:
        formentries = entries_of_this_type.filter(sec_path=sec_path)

        # Below adds up the transactions on the forms and rolls forward the
        # shares held for this form.
        shares_acquired_disposed =\
            formentries.exclude(xn_acq_disp_code=None)\
            .values_list('xn_acq_disp_code', 'transaction_shares')
        form_transaction_shares =\
            transaction_share_calculator(shares_acquired_disposed)
        shares_held += form_transaction_shares

        non_xn_form_shares_remaining = \
            formentries.filter(transaction_shares=None)\
            .aggregate(Sum('reported_shares_following_xn'))

        # Below grabs the last transaction and adds the shares remaining to the
        # holdings above.  The rationale is we don't know how many transactions
        # were in the same security, but we know the last transaction is likely
        # distinct from the holdings reported with no transaction.  (Otherwise
        # the holdings would not have been reported -- why say "I sold 20 and
        # 10 remaining" and then also say "I have 10 remaining"? -- that would
        # be weird and thats how we know the last transaction is unlikely to
        # be a reported holding.  We don't use all transaction shares remaining
        # because these regularly are in the same pile of stock.)

        xn_form_entries = \
            formentries.exclude(transaction_shares=None)
        if xn_form_entries.exists():
            xn_form_shares_remaining =\
                xn_form_entries.order_by('-transaction_number')[0]\
                .reported_shares_following_xn
        else:
            xn_form_shares_remaining = 0
        form_entry_min_shares_remaining =\
            non_xn_form_shares_remaining + xn_form_shares_remaining

        shares_following_xn = \
            max(shares_held,
                form_entry_min_shares_remaining)

        formentries_by_xn_number =\
            formentries.order_by('transaction_number')
        shares_remaining_prior_to_form =\
            shares_following_xn - form_transaction_shares
        temp_shares_remaining = shares_remaining_prior_to_form
        for formentry in formentries_by_xn_number:
            xn_acq_disp_code = formentry.xn_acq_disp_code
            transaction_shares = formentry.transaction_shares
            if xn_acq_disp_code == 'A':
                temp_shares_remaining += transaction_shares
            if xn_acq_disp_code == 'D':
                temp_shares_remaining -= transaction_shares
            formentry.shares_following_xn = temp_shares_remaining
            formentry.save()

        shares_held = shares_following_xn

    entries_of_this_type.update(shares_following_xn_is_adjusted=True)
