from sdapp.models import Form345Entry, Affiliation
import os
import sys
from decimal import Decimal

affiliations_and_securities_with_unadjusted_indirect_entries = \
    Form345Entry.objects.filter(shares_following_xn_is_adjusted=False)\
    .filter(direct_or_indirect='I')\
    .values_list('affiliation',
                 'short_sec_title',
                 'scrubbed_underlying_title',
                 'expiration_date',
                 'direct_or_indirect')\
    .distinct()


for entrydata in affiliations_and_securities_with_unadjusted_indirect_entries:
    affiliation,\
        short_sec_title,\
        scrubbed_underlying_title,\
        expiration_date,\
        direct_or_indirect\
        = entrydata
# This query generates the matrix we will use to adjust each entry
    forms_of_this_type =\
        Form345Entry.objects.filter(affiliation=affiliation)\
        .filter(short_sec_title=short_sec_title)\
        .filter(scrubbed_underlying_title=scrubbed_underlying_title)\
        .filter(expiration_date=expiration_date)\
        .filter(direct_or_indirect=direct_or_indirect)
    form_matrix = \
        forms_of_this_type\
        .order_by('supersededdt')\
        .values_list('pk',
                     'sec_path',
                     'transaction_shares',
                     'xn_acq_disp_code',
                     'reported_shares_following_xn',
                     'filedatetime',
                     'supersededdt')
    distinct_sec_paths = list(set(zip(*form_matrix)[1]))
    sec_path_total_dict = {}
    for sec_path in distinct_sec_paths:
        sec_path_holdings = \
            forms_of_this_type.filter(sec_path=sec_path)\
            .filter(transaction_shares=None)\
            .values_list('reported_shares_following_xn', flat=True)
        form_holding_sum = sum([x for x in sec_path_holdings if x is not None])
        # This grabs the last transaction and adds the shares remaining to the 
        # holdings above.  The rationale is we don't know how many transactions
        # were in the same security, but we know the last transaction is likely
        # distinct from the holdings reported with no transaction.  (Otherwise
        # the holdings would not have been reported -- why say "I sold 20 and
        # 10 remaining" and then also say "I have 10 remaining"? -- that would
        # be weird and thats how we know the last transaction is unlikely to 
        # be a reported holding.  We don't use all transaction shares remaining
        # because these regularly are in the same pile of stock.)
        sec_path_transactions = \
            forms_of_this_type.filter(sec_path=sec_path)\
            .exclude(transaction_shares=None)\
            .exclude(reported_shares_following_xn=None)\
            .order_by('-transaction_number')
        if sec_path_transactions.exists():
            sec_path_last_transaction_holding =\
                sec_path_transactions[0].reported_shares_following_xn
        else:
            sec_path_last_transaction_holding = Decimal(0)
        form_total_holdings = form_holding_sum +\
            sec_path_last_transaction_holding
        sec_path_total_dict[sec_path] = form_total_holdings

    new_form_matrix = []
    for entry in form_matrix:
        entry_sec_path = entry[1]
        list_entry = list(entry)
        list_entry.append(sec_path_total_dict[sec_path])
        new_form_matrix.append(list_entry)


