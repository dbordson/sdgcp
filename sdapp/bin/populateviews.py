from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry,\
    Affiliation, ClosePrice, SecurityPriceHist, SplitOrAdjustmentEvent
# from django.db import connection
import datetime
from operator import mul


def weighted_avg(conversion_price_unit_list):
    dotproduct = sum(p * q for p, q in conversion_price_unit_list)
    divisor = sum(weightingvector)
    wavg = dotproduct / divisor
    return wavg


def wavgdate(expiration_date_unit_list):
    try:
        datevector, unit_vector = zip(*expiration_date_unit_list)
        today = datetime.date.today()
        tdvector = [float((entry - today).days) for entry in datevector]
        # the below line doesn't work with single entry lists
        if len(tdvector) == 1:
            return (today + datetime.timedelta(tdvector[0]))
        dotproduct = sum(float(p) * float(q)
                         for p, q in zip(tdvector, unit_vector))
        denominator = sum(unit_vector)
        wavgdelta = dotproduct / float(denominator)
        wavg = today + datetime.timedelta(wavgdelta)
        return wavg
    except:
        return None


def intrinsicvalcalc(conversion_price_unit_list, underlyingprice):
    conv_vector, unitsvector =\
        zip(*conversion_price_unit_list)

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


def nonderiv_adjusted_total(split_security_id, date_and_holding_entries):
    date_and_holding_entries_as_list =\
        [list(row) for row in date_and_holding_entries]
    split_adj_list = SplitOrAdjustmentEvent.objects\
        .filter(security=security_id)\
        .values_list('event_date', 'adjustment_factor')
    adjustment_entries = [list(row) for row in split_adj_list]
    adjusted_total_shares = 0
    unadjusted_shares = 0
    for holding_date, shares_held in date_and_holding_entries_as_list:
        adjustment_list_for_holding =\
            [splitfactor for splitdate, splitfactor in adjustment_entries
                if splitdate >= holding_date]
        adjustment_factor = reduce(mul, adjustment_list_for_holding, 1)
        adjusted_total_shares += shares_held * adjustment_factor
    return adjusted_total_shares


def pub_stock_value_calculator(security_id):
    price = \
        ClosePrice.objects\
        .filter(securitypricehist__security_id=security_id)\
        .latest('close_date').adj_close_price
    split_events = \
        SplitOrAdjustmentEvent.objects\
        .filter(security=security_id)
    # Note that this logic equates the period of report to the
    # date of the transaction.  This could create problems for
    # transactions occuring near a stock split.
    date_and_holding_entries = Form345Entry.objects\
        .filter(supersededdt=None)\
        .filter(security=security_id)\
        .values_list('period_of_report', 'shares_following_xn')
    adjusted_shares =\
        nonderiv_adjusted_total(security_id, date_and_holding_entries)
    try:
        intrinsicvalue = price * adjusted_shares
        return intrinsicvalue, adjusted_shares
    except:
        return 'Not Available'


def deriv_adj_total_and_conv(split_security_id,
                             date_and_conv_and_holding_entries):
    form_entries_as_list =\
        [list(row) for row in date_and_conv_and_holding_entries]
    split_adj_list = SplitOrAdjustmentEvent.objects\
        .filter(security=security_id)\
        .values_list('event_date', 'adjustment_factor')
    adjustment_entries = [list(row) for row in split_adj_list]
    adjusted_total_shares = 0
    unadjusted_shares = 0
    adjusted_conv_and_holdings_list = []
    for holding_date, conversion_price, shares_held in form_entries_as_list:
        adjustment_list_for_holding =\
            [splitfactor for splitdate, splitfactor in adjustment_entries
                if splitdate >= holding_date]
        adjustment_factor = float(reduce(mul, adjustment_list_for_holding, 1))
        adjusted_conv_and_holdings =\
            [conversion_price / adjustment_factor,
             shares_held * adjustment_factor]
        adjusted_conv_and_holdings_list.append(adjusted_conv_and_holdings)

    return adjusted_conv_and_holdings_list


def deriv_value_calculator(security_id):
    security = Security.objects.get(id=security_id)
    underlying_security_title =\
        security.scrubbed_underlying_title
    cik = security.issuer
    underlying_security_set = Security.objects.filter(issuer=cik)\
        .filter(short_sec_title=underlying_security_title)
    if underlying_security_set.exists() and\
            underlying_security_set[0].ticker is not None:
        price = \
            ClosePrice.objects\
            .filter(securitypricehist__security=underlying_security_set[0].id)\
            .latest('close_date')\
            .adj_close_price
        split_events = \
            SplitOrAdjustmentEvent.objects\
            .filter(security=underlying_security_set[0].id)
        date_and_conv_and_holding_entries = Form345Entry.objects\
            .filter(supersededdt=None)\
            .filter(security=security_id)\
            .exclude(shares_following_xn=0)\
            .values_list('period_of_report',
                         'conversion_price',
                         'shares_following_xn')
        conversion_price_unit_list = \
            deriv_adj_conv_and_total(underlying_security_set[0].id,
                                     date_and_conv_and_holding_entries)
        conversion_factor = 1
        intrinsic_value = \
            conversion_factor *\
            intrinsicvalcalc(conversion_price_unit_list, price)
        # NEED TO INSERT CONVERSION FACTOR

        # next need to build vector of prices and adjustment dates
    return None


def build_security_views():
    print 'Building SecurityView objects'
    print '    Sorting...',
    security_ids = Form345Entry.objects.filter(supersededdt=None)\
        .values_list('security', flat=True).distinct()
    for security_id in security_ids:
        latest_transaction =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security=security_id)\
            .latest('filedatetime')
        sec_obj = Securty.objects.get(pk=security_id)
        today = datetime.date.today()
        # expiration date searches / calculations
        expiration_date_unit_list =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .exclude(expiration_date__lte=today)\
            .exclude(expiration_date=None)\
            .values_list('expiration_date', 'underlying_shares')
        expdatevector, expunit_vector = zip(*expiration_date_unit_list)
        wavg_exp_date = wavgdate(expiration_date_unit_list)
        if len(expiration_date_unit_list) > 0:
            expdatevector, expunit_vector = zip(*expiration_date_unit_list)
            first_expiration_date = min(expdatevector)
            last_expiration_date = max(expdatevector)
        else:
            first_expiration_date = None
            last_expiration_date = None
        # transaction price searches / calculations
        xndatevector =\
            Form345Entry.objects\
            .filter(security_id=security_id)\
            .exclude(transaction_date=None)\
            .values_list('transaction_date')
        if len(xndatevector) > 0:
            first_transaction_date = min(xndatevector)
            last_transaction_date = max(xndatevector)
        else:
            first_transaction_date = None
            last_transaction_date = None

        # conversion price searches / calculations
        # first, do we have a price for it
        if sec_obj.deriv_or_nonderiv == 'N' and\
                sec_obj.ticker is not None:
            intrinsicvalue, units_held =\
                pub_stock_value_calculator(security_id)
        elif sec_obj.deriv_or_nonderiv == 'D':
            intrinsic_value =\
                deriv_value_calculator  (security_id)


        # conversion_price_unit_list =\
        #     Form345Entry.objects.filter(supersededdt=None)\
        #     .filter(security_id=security_id)\
        #     .exclude(conversion_price=None)\
        #     .values_list('conversion_price', 'underlying_shares')
        # weighted_avg_conversion = weighted_avg(conversion_price_unit_list)
        # if len(conversion_price_unit_list) > 0:
        #     convpricevector, convunit_vector = zip(*conversion_price_unit_list)
        #     min_conversion_price = min(convpricevector)
        #     max_conversion_price = max(convpricevector)
        # else:
        #     min_conversion_price = None
        #     max_conversion_price = None

        # underlying shares, intrinsic value
        # get the ticker for the underlying security?
        conversion_price_unit_list =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .exclude(conversion_price=None)\
            .values_list('conversion_price',
                         'underlying_shares',
                         'scrubbed_underlying_title')
        security_view_object =\
            SecurityView(issuer=sec_obj.issuer,
                         short_sec_title=sec_obj.short_sec_title,
                         ticker=sec_obj.ticker,
                         units_held=,
                         deriv_or_nonderiv=sec_obj.deriv_or_nonderiv,
                         first_expiration_date=first_expiration_date,
                         last_expiration_date=last_expiration_date,
                         wavg_expiration_date=wavg_exp_date,
                         min_conversion_price=min_conversion_price,
                         max_conversion_price=max_conversion_price,
                         wavg_conversion=weighted_avg_conversion,
                         scrubbed_underlying_title=
                         sec_obj.scrubbed_underlying_title,
                         underlying_shares=,
                         intrinsic_value=,
                         first_xn=first_transaction_date,
                         most_recent_xn=last_transaction_date)










