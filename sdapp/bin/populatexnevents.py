from sdapp.models import Form345Entry, ClosePrice,\
    SecurityPriceHist, TransactionEvent, SplitOrAdjustmentEvent
import datetime
from decimal import Decimal
import bisect
import pytz
from operator import mul

print "Starting regression analysis;"
print "organizing input objects..."
a = Form345Entry.objects\
    .exclude(transaction_shares=None)\
    .exclude(transaction_date=None)\
    .values_list('issuer_cik',
                 'security',
                 'affiliation',
                 'xn_acq_disp_code',
                 'transaction_code',
                 'transaction_shares',
                 'transaction_date')


def period_tuple_lister():
    years_considered = 5
    start_tuples = \
        [(1, 1),
         (4, 1),
         (7, 1),
         (10, 1)]
    end_tuples = \
        [(3, 31),
         (6, 30),
         (9, 30),
         (12, 31)]
    today = datetime.date.today()
    todaymonth = today.month
    todayday = today.day
    todaytuple = (todaymonth, todayday)
    year = today.year
    current_quarter_tuple_index = bisect.bisect_left(end_tuples, todaytuple)
    tuple_index = current_quarter_tuple_index
    count = years_considered * 4
    periodspans = []
    for x in range(count):
        if tuple_index == 0:
            tuple_index = 3
            year -= 1
        else:
            tuple_index -= 1
        periodspans.append([start_tuples[tuple_index],
                            end_tuples[tuple_index],
                            year
                            ])
        x += 1
    return periodspans


def ad(acq_disp):
    if acq_disp == 'D':
        ad = -1
    else:
        ad = 1
    return ad


def zerofill(conversion_price):
    if conversion_price is None:
        conversion_price = Decimal(0)
    return conversion_price


def xnvalcalc(units_xcted_acq_disp_and_conv_vectors, dp_lists):
    # The below loop is values stocks and options with the
    # stock as the underlying security.  Input should be filtered
    # accordingly.
    xns_val = Decimal(0)
    for units, date, acq_disp, conv_price, conv_mult\
            in units_xcted_acq_disp_and_conv_vectors:
        # print "units, date, acq_disp, conv_price, conv_mult",
        # print units, date, acq_disp, conv_price, conv_mult
        price = dp_lists[1][bisect.bisect_left(dp_lists[0], date)]
        # print dp_lists[0][bisect.bisect_left(dp_lists[0], date)]
        # print date
        # print price
        xns_val += \
            max((price - zerofill(conv_price)), Decimal(0.0))\
            * units * conv_mult * ad(acq_disp)
    return xns_val


def intrinsicvalcalc(units_held_and_adj_and_conv_vectors,
                     period_adj_factor,
                     close_price_at_end_datetime):
    if close_price_at_end_datetime is None:
        return None
    intrinsicval = Decimal(0)
    price = close_price_at_end_datetime
    for shares_held, holding_adjustment_factor, conv_price, conv_mult\
            in units_held_and_adj_and_conv_vectors:
        # print "units, date, acq_disp, conv_price, conv_mult",
        # print units, date, acq_disp, conv_price, conv_mult
        # print price
        intrinsicval += \
            max((price - zerofill(conv_price)), Decimal(0.0))\
            * shares_held * conv_mult\
            * holding_adjustment_factor / period_adj_factor
    return intrinsicval


def later_price(sec_price_hist, end_date, ep, td_days):
    td = datetime.timedelta(td_days)
    qs_at_td_days =\
        ClosePrice.objects\
        .filter(securitypricehist=sec_price_hist)\
        .filter(close_date__lt=end_date + td)\
        .filter(close_date__gte=end_date + td - datetime.timedelta(5))\
        .order_by('-close_date')
    # print 'end_date, ep, td_days, td'
    # print end_date, ep, td_days, td

    if qs_at_td_days.exists() and ep is not None:
        price_at_td_days = qs_at_td_days[0].adj_close_price
        performance = (price_at_td_days / ep) - 1
    else:

        performance = None
    # print performance
    return performance


def period_queries(issuer, start_datetime, end_datetime,
                   sec_price_hist, unadj_date_price_lists):
    period_entries =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(is_officer=True)\
        .filter(filedatetime__gte=start_datetime)\
        .filter(filedatetime__lt=end_datetime)\
        .exclude(form_type='3/A')\
        .exclude(form_type='4/A')\
        .exclude(form_type='5/A')\
        .exclude(transaction_shares=None)\
        .exclude(transaction_date=None)
    period_xns_values =\
        period_entries\
        .values_list('transaction_shares',
                     'transaction_date',
                     'xn_acq_disp_code',
                     'conversion_price',
                     'security__conversion_multiple')
    net_xn_val = xnvalcalc(period_xns_values, unadj_date_price_lists)
    ending_entries =\
        Form345Entry.objects.filter(issuer_cik=issuer)\
        .filter(is_officer=True)\
        .filter(supersededdt__gt=end_datetime)\
        .filter(filedatetime__lte=end_datetime)\
        .exclude(shares_following_xn=None)
    ending_holding_values =\
        ending_entries\
        .values_list('shares_following_xn',
                     'adjustment_factor',
                     'conversion_price',
                     'security__conversion_multiple')

    end_date = end_datetime.date()
    close_price_obj_at_end_datetime =\
        ClosePrice.objects\
        .filter(securitypricehist=sec_price_hist)\
        .filter(close_date__lt=end_date)\
        .order_by('-close_date')
    if close_price_obj_at_end_datetime.exists():
        close_price_at_end_datetime =\
            close_price_obj_at_end_datetime[0].close_price
        price_at_period_end =\
            close_price_obj_at_end_datetime[0].adj_close_price
    else:
        close_price_at_end_datetime = None
        price_at_period_end = None

    end_period_adj_factors =\
        SplitOrAdjustmentEvent.objects\
        .filter(security=sec_price_hist.security)\
        .filter(event_date__gt=end_date)\
        .values_list('adjustment_factor', flat=True)
    period_adj_factor = reduce(mul, end_period_adj_factors, Decimal(1.0))

    end_holding_val =\
        intrinsicvalcalc(ending_holding_values, period_adj_factor,
                         close_price_at_end_datetime)

    if end_holding_val == Decimal(0) or\
            end_holding_val is None:
        net_xn_pct = None
    else:
        net_xn_pct = net_xn_val / end_holding_val
    ep = price_at_period_end
    # print 'end_holding_val, end_datetime'
    # print end_holding_val, end_datetime
    perf_at_91_days = later_price(sec_price_hist, end_date, ep, 91)
    perf_at_182_days = later_price(sec_price_hist, end_date, ep, 182)
    perf_at_274_days = later_price(sec_price_hist, end_date, ep, 274)
    perf_at_365_days = later_price(sec_price_hist, end_date, ep, 365)
    perf_at_456_days = later_price(sec_price_hist, end_date, ep, 456)

    new_xn_event =\
        TransactionEvent(issuer_id=issuer,
                         net_xn_val=net_xn_val,
                         end_holding_val=end_holding_val,
                         net_xn_pct=net_xn_pct,
                         period_start=start_datetime.date(),
                         period_end=end_datetime.date(),
                         price_at_period_end=price_at_period_end,
                         perf_at_91_days=perf_at_91_days,
                         perf_at_182_days=perf_at_182_days,
                         perf_at_274_days=perf_at_274_days,
                         perf_at_365_days=perf_at_365_days,
                         perf_at_456_days=perf_at_456_days)
    return new_xn_event


periodspans = period_tuple_lister()
issuers =\
    SecurityPriceHist.objects\
    .values_list('issuer', flat=True)\
    .distinct()
# significance_aggregate = Decimal(100 * 1000)
# significance_percent = Decimal(0.20)

TransactionEvent.objects.all().delete()
events_to_save = []
totalissuers = len(issuers)
count = 0
for issuer in issuers:
    count += 1
    print "Issuer CIK:", issuer
    print count, "of", totalissuers
    sec_price_hist =\
        SecurityPriceHist.objects.filter(issuer=issuer)[0]
    unadj_date_price_lists = \
        zip(*ClosePrice.objects.filter(securitypricehist=sec_price_hist)
            .order_by('close_date')
            .values_list('close_date', 'close_price'))
    for period in periodspans:
        (start_mo, start_day), (end_mo, end_day), year = period
        start_datetime =\
            datetime.datetime(year, start_mo, start_day, tzinfo=pytz.UTC)
        end_datetime =\
            datetime.datetime(year, end_mo, end_day, tzinfo=pytz.UTC)\
            + datetime.timedelta(1)

        new_xn_event = \
            period_queries(issuer, start_datetime, end_datetime,
                           sec_price_hist, unadj_date_price_lists)
        events_to_save.append(new_xn_event)
    TransactionEvent.objects.bulk_create(events_to_save)
    events_to_save = []

print "TransactionEvent objects saved.  Done"


# xn_layover_days = 30
# tdelt = datetime.timedelta(days=-xn_layover_days)

# for reporting_owner, issuer in affiliations:
#     a = Form345Entry.objects\
#         .filter(issuer_cik_num=issuer)\
#         .filter(is_officer=True)\
#         .filter(reporting_owner=reporting_owner)\
#         .exclude(transaction_shares=None)\
#         .exclude(transaction_date=None)\
#         .values_list('issuer_cik',
#                      'security',
#                      'affiliation',
#                      'xn_acq_disp_code',
#                      'transaction_code',
#                      'transaction_shares',
#                      'filedatetime')
#     for row in a:
#         prior_xns = Form345Entry.objects\
#             .filter(issuer_cik_num=issuer)\
#             .filter(reporting_owner=reporting_owner)\
#             .filter(filedatetime_lte=row[6])\
#             .filter(filedatetime_gt=row[6] + tdelt)\
#             .filter(is_officer=True)\
#             .exclude(transaction_shares=None)\
#             .exclude(transaction_date=None)\
#             .values_list('security',
#                          'xn_acq_disp_code',
#                          'transaction_code',
#                          'transaction_shares')
#         # INSERT FUNCTION TO TURN THIS INTO NET XN AMT
#         xn_event =\
#             TransactionEvent(issuer=issuer,
#                              reporting_person=reporting_owner,

#             )

# dCPs = {}
# dCPsIndex = {}
# dCPsValues = {}
# for issuer in issuers:
#     issuercloseprices =\
#         ClosePrice.objects\
#         .filter(securitypricehist__issuer=issuer)\
#         .exclude(adj_close_price=None)\
#         .exclude(close_date=None)
#     dCPs[issuer] = {}

#     dCPsIndex[issuer] =\
#         issuercloseprices\
#         .order_by('close_date')\
#         .values_list('close_date', flat=True)

#     dCPsValues[issuer] =\
#         issuercloseprices\
#         .order_by('close_date')\
#         .values_list('adj_close_price', flat=True)

#     CPs =\
#         issuercloseprices\
#         .values('close_date',
#                 'adj_close_price')
#     for CP in CPs:
#         dCPs[issuer][CP['close_date']] = CP['adj_close_price']


# newa = []
# for item in a:
#     issuer = item[0]
#     close_date = item[4]
#     adj_close_price = None
#     if issuer in dCPs:
#         if close_date in dCPs[issuer]:
#             adj_close_price = dCPs[issuer][close_date]
#     listrow = list(item)
#     listrow.append(adj_close_price)
#     newa.append(listrow)
# a = newa

# b = zip(*a)
# d = {'issuer_cik': list(b[0]),
#      'security': list(b[1]),
#      'affiliation': list(b[2]),
#      'transaction_shares': list(b[3]),
#      'transaction_date': pandas.to_datetime(pandas.Series(list(b[4]))),
#      'adj_close_price': list(b[5])}
# transaction_data = pandas.DataFrame(d)\
#     .sort('transaction_date', ascending=False)
# print transaction_data.head()
