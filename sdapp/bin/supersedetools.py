from sdapp.models import Form345Entry, Affiliation
import datetime
from decimal import Decimal
import django.db
from django.db.models import Max


def convert_date_to_datetimestring(date):
    c = str(date)
    return c[:10] + " 23:59:59Z"


def reset_database_connection():
    django.db.close_connection()


# NOT IN USE -- COULD BE USED TO try to speed up by bulk updating
# THE CHALLENGE WOULD BE TO GET DATE IN WITH TIME ZONE
# def bulk_update(pk_supersededdt_pairs):
#     c = django.db.connection.cursor()
#     BUILD BIG SQL INSTRUCTIONS TO SEND TO UPDATE A BLOCK OF ITEMS
#     c.execute('UPDATE form345entry SET supersededdt= WHERE sdapp_form345entry.id = %s;' % 2405637)

def string_date_with_years_added(yearsafter, date_in_iso):
    c = date_in_iso
    if c[4:10] == '-02-29':
        return str(int(c[0:4]) + yearsafter) + '-03-01' + " " + c[11:19] + "Z"
    return str(int(c[0:4]) + yearsafter) + c[4:10] + " " + c[11:19] + "Z"


def set_supersededdt(pk, supersededdt):
    Form345Entry.objects.filter(pk=pk).update(supersededdt=supersededdt)
    # a = Form345Entry.objects.get(pk=pk)
    # a.supersededdt = supersededdt
    # print supersededdt
    # a.save()
    # a = 0
    return


def calc_max_superseded_xn_date(chain_entries_incl_superseded):
    # Here we get teh max superseded xn date to determine whether the early
    # unsuperseded filings were stale when filed.
    last_superseded_xn_date_in_chain =\
        chain_entries_incl_superseded.exclude(supersededdt=None)\
        .exclude(transaction_date=None)\
        .aggregate(Max('transaction_date'))['transaction_date__max']
    if last_superseded_xn_date_in_chain is not None:
        last_superseded_xn_date = last_superseded_xn_date_in_chain
    else:
        last_superseded_xn_date = datetime.date(1900, 1, 1)
    # This handles holdings (if a holding was filed on 2/1 and then a
    # transaction on 1/20 is reported later, this infor is already stale
    # because the filedatetime is what matters for holdings)
    last_superseded_holding_dt_in_chain =\
        chain_entries_incl_superseded.exclude(supersededdt=None)\
        .filter(transaction_date=None)\
        .aggregate(Max('filedatetime'))['filedatetime__max']
    if last_superseded_holding_dt_in_chain is not None:
        last_superseded_holding_date =\
            last_superseded_holding_dt_in_chain.date()
    else:
        last_superseded_holding_date = datetime.date(1900, 1, 1)
    max_superseded_xn_date = max(last_superseded_xn_date,
                                 last_superseded_holding_date)
    return max_superseded_xn_date


def calc_supersededdts_for_chains(affiliation,
                                  short_sec_title, expiration_date,
                                  direct_or_indirect):
    chain_entries_incl_superseded =\
        Form345Entry.objects.filter(affiliation=affiliation)\
        .filter(short_sec_title=short_sec_title)\
        .filter(expiration_date=expiration_date)\
        .filter(direct_or_indirect=direct_or_indirect)

    max_superseded_xn_date = \
        calc_max_superseded_xn_date(chain_entries_incl_superseded)

    chain_entries_excl_superseded_and_ordered =\
        chain_entries_incl_superseded.filter(supersededdt=None)\
        .order_by('filedatetime', 'transaction_number')\
        .values_list('pk', 'filedatetime', 'transaction_date',
                     'shares_following_xn')
    django.db.reset_queries()
    max_preceding_transaction_date = max_superseded_xn_date
    if max_preceding_transaction_date is None:
        max_preceding_transaction_date = datetime.date(1900, 1, 1)
    sequential_list_of_entries = []
    for pk, filedatetime, transaction_date, shares_following_xn\
            in chain_entries_excl_superseded_and_ordered:

        if transaction_date is None:
            transaction_date = filedatetime.date()
        # Build sequential list of transactions
        if transaction_date >= max_preceding_transaction_date:
            sequential_list_of_entries\
                .append([pk, filedatetime, transaction_date,
                        shares_following_xn])
            max_preceding_transaction_date = transaction_date
            # This will properly handle form 4/As, except in the
            # (I think) unlikely edge case where the form 4/A is
            # amending the date of the transaction to be earlier
            # than originally reported.
        else:
            set_supersededdt(pk, filedatetime)

    reverse_chrono_sequential_list = sequential_list_of_entries[::-1]

    # HOW POSSIBLE TO BE LEN = 0?
    if len(reverse_chrono_sequential_list) > 0:
        # sets succeeding_filedatetime to most recent entry
        succeeding_filedatetime = reverse_chrono_sequential_list[0][1]
        today = datetime.date.today()
    # determines whether should be superseded because of expiration;
    # the +5 gives time delay for filing form 4 recording exercise /
    # forfeiture due to expiration.
        if expiration_date is not None\
                and expiration_date + datetime.timedelta(5) < today:
            pk = reverse_chrono_sequential_list[0][0]
            set_supersededdt(pk,
                             convert_date_to_datetimestring(expiration_date))
        # removes most recent so it won't be set as superseded
        reverse_chrono_sequential_list.pop(0)

    for pk, filedatetime, transaction_date, shares_following_xn\
            in reverse_chrono_sequential_list:
        if shares_following_xn != Decimal(0):
            set_supersededdt(pk, succeeding_filedatetime)
        else:
            set_supersededdt(pk, filedatetime)
        succeeding_filedatetime = filedatetime

    return


def supersede_stale_entries(cutoff_years, is_officer):
    today = datetime.date.today()
    cutoffdatetime =\
        today - datetime.timedelta(cutoff_years * 365)
    staleness_delay = datetime.timedelta(cutoff_years * 365)

    # Figure out why this is screwing up thomas watjen's numbers?
    # THE BELOW IS CALCULATING THE MAX FILEDATETIME FOR ALL
    # FORM345ENTRY OBJECTS?
    # WILL NEED TO DO BY AFFILIATION?
    # stale_affiliation_list =\
    #     Form345Entry.objects.filter(supersededdt=None)\
    #     .exclude(affiliation=None)\
    #     .filter(is_officer=is_officer)\
    #     .annotate(Max('filedatetime'))\
    #     .filter(filedatetime__max__lt=cutoffdatetime)\
    #     .values_list('affiliation', 'filedatetime__max')\
    #     .distinct()

    affiliation_list =\
        Affiliation.objects.filter(form345entry__supersededdt=None)
    # stale_affiliation_list =\
    #     Affiliation.objects.filter(form345entry__supersededdt=None)\
    #     .filter()\
    #     .annotate(Max('filedatetime'))
    looplength = float(len(affiliation_list))
    counter = 0.0
    for affiliation in affiliation_list:
        relevant_forms =\
            Form345Entry.objects.filter(affiliation=affiliation)\
            .filter(supersededdt=None).filter(is_officer=is_officer)
        latest_filedatetime =\
            relevant_forms.aggregate(Max('filedatetime'))['filedatetime__max']
        if latest_filedatetime is not None\
                and latest_filedatetime.date() < cutoffdatetime:
            staleness_datetime =\
                convert_date_to_datetimestring(
                    latest_filedatetime + staleness_delay)
            Form345Entry.objects.filter(affiliation=affiliation)\
                .filter(supersededdt=None).filter(is_officer=is_officer)\
                .update(supersededdt=staleness_datetime)

    # for affiliation, filedatetime__max in stale_affiliation_list:
    #     staleness_datetime =\
    #     convert_date_to_datetimestring(filedatetime__max + staleness_delay)
    #     Form345Entry.objects.filter(supersededdt=None)\
    #         .filter(affiliation=affiliation)\
    #         .filter(is_officer=is_officer)\
    #         .update(supersededdt=staleness_datetime)
        if float(int(10*counter/looplength)) !=\
                float(int(10*(counter-1)/looplength)):
            print int(counter/looplength*100), 'percent'
        counter += 1.0
    return
