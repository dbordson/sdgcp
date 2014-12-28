from sdapp.models import Form345Entry, ClosePrice, Security, SecurityView,\
    Affiliation, PersonHoldingView
# from django.db import connection
import datetime
from decimal import Decimal


def calc_weighted_avg_conversion(units_held_and_adj_and_conv_vectors):
    unitsvector, adjustment_vector, conv_vector =\
        zip(*units_held_and_adj_and_conv_vectors)
    value_and_units_vectors =\
        [[conv_price / adjustment,
          units * adjustment]
         for units, adjustment, conv_price
         in units_held_and_adj_and_conv_vectors]
    if len(value_and_units_vectors) == 1:
        return value_and_units_vectors[0][0]
    else:
        dotproduct = sum(p * q for p, q in value_and_units_vectors)
        divisor = sum(q for p, q in value_and_units_vectors)
        wavg = dotproduct / divisor
        return wavg


def wavgdate(expiration_date_unit_list):
    # try:
    if len(expiration_date_unit_list) == 1:
        return expiration_date_unit_list[0][0]

    datevector, unit_vector, adjustment_vector = \
        zip(*expiration_date_unit_list)
    today = datetime.date.today()
    tdvector = [float((entry - today).days) for entry in datevector]
    adj_unit_vector = \
        [units * adjustment for units, adjustment
         in zip(unit_vector, adjustment_vector)]
    dotproduct = sum(float(p) * float(q)
                     for p, q in zip(tdvector, adj_unit_vector))
    denominator = sum(adj_unit_vector)
    wavgdelta = dotproduct / float(denominator)
    wavg = today + datetime.timedelta(wavgdelta)
    return wavg
    # except:
    #     return None


def intrinsicvalcalc(units_held_and_adj_and_conv_vectors,
                     conversion_multiple,
                     underlyingprice):
    # conversion_price_unit_list, underlyingprice):
    unitsvector, adjustment_vector, conv_vector =\
        zip(*units_held_and_adj_and_conv_vectors)
    # print units_held_and_adj_and_conv_vectors
    up = underlyingprice
    # print up
        # The below list comprehension is finding in the money options
        # and the number of shares each converts into.
    value_and_units_vectors =\
        [[max((up - (conv_price / adjustment)), Decimal(0.0)),
          units * adjustment * conversion_multiple]
         for units, adjustment, conv_price
         in units_held_and_adj_and_conv_vectors]
    if len(value_and_units_vectors) == 1:
        return value_and_units_vectors[0][0] * value_and_units_vectors[0][1]
    else:
        dotproduct =\
            sum(p * q for p, q in value_and_units_vectors)
        return dotproduct


def build_security_views():
    print 'Building SecurityView objects'
    print '    Sorting and linking...',
    security_view_objects = []
    security_ids = Form345Entry.objects.filter(supersededdt=None)\
        .values_list('security', flat=True).distinct()
    for security_id in security_ids:
        latest_transaction =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security=security_id)\
            .latest('filedatetime')
        if latest_transaction.underlying_security is not None:
            underlying_ticker = latest_transaction.underlying_security.ticker
        else:
            underlying_ticker = None
        sec_obj = Security.objects.get(pk=security_id)
        today = datetime.date.today()
        # expiration date searches / calculations
        # Maybe check this to set None expiration date to far in future
        expiration_date_unit_list =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .exclude(expiration_date__lte=today)\
            .exclude(underlying_shares=0)\
            .exclude(underlying_shares=None)\
            .exclude(expiration_date=None)\
            .values_list('expiration_date',
                         'underlying_shares',
                         'adjustment_factor')
        if len(expiration_date_unit_list) > 0:
            wavg_exp_date = wavgdate(expiration_date_unit_list)
            expdatevector, expunit_vector, adjustment_vector = \
                zip(*expiration_date_unit_list)
            first_expiration_date = min(expdatevector)
            last_expiration_date = max(expdatevector)
        else:
            wavg_exp_date = None
            first_expiration_date = None
            last_expiration_date = None
        # transaction price searches / calculations
        xndatevector =\
            Form345Entry.objects\
            .filter(security_id=security_id)\
            .filter(supersededdt=None)\
            .exclude(transaction_date=None)\
            .values_list('transaction_date', flat=True)
        if len(xndatevector) > 0:
            first_transaction_date = min(xndatevector)
            last_transaction_date = max(xndatevector)
        else:
            first_transaction_date = None
            last_transaction_date = None

        # units held calculation (adjusted for splits)
        units_held_and_adjustment_vectors =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .exclude(shares_following_xn=None)\
            .exclude(shares_following_xn=0)\
            .exclude(adjustment_factor=None)\
            .values_list('shares_following_xn',
                         'adjustment_factor')
        if len(units_held_and_adjustment_vectors) == 0:
            units_held = 0
        elif len(units_held_and_adjustment_vectors) == 1:
            units_held = \
                units_held_and_adjustment_vectors[0][0] *\
                units_held_and_adjustment_vectors[0][1]
        else:
            dotproduct = sum(p * q for p, q in
                             units_held_and_adjustment_vectors)
            units_held = dotproduct

        if sec_obj.deriv_or_nonderiv == 'N' and\
                sec_obj.ticker is not None:
            price = \
                ClosePrice.objects\
                .filter(securitypricehist__security_id=security_id)\
                .latest('close_date').adj_close_price
            intrinsic_value =\
                units_held * price
            last_close_price = price
            underlying_close_price = None
        elif sec_obj.deriv_or_nonderiv == 'D' and\
                underlying_ticker is not None:
            # print security_id
            units_held_and_adj_and_conv_vectors =\
                Form345Entry.objects.filter(supersededdt=None)\
                .exclude(shares_following_xn=0)\
                .exclude(shares_following_xn=None)\
                .filter(security_id=security_id)\
                .values_list('shares_following_xn',
                             'adjustment_factor',
                             'conversion_price')

            underlyingprice = \
                ClosePrice.objects\
                .filter(securitypricehist__security_id=
                        latest_transaction.underlying_security)\
                .latest('close_date').adj_close_price
            intrinsic_value =\
                intrinsicvalcalc(units_held_and_adj_and_conv_vectors,
                                 sec_obj.conversion_multiple,
                                 underlyingprice)
            last_close_price = None
            underlying_close_price = underlyingprice
        else:
            intrinsic_value = None
            last_close_price = None
            underlying_close_price = None

        weighted_avg_conversion = None
        min_conversion_price = None
        max_conversion_price = None
        units_held_and_adj_and_conv_vectors =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .exclude(shares_following_xn=0)\
            .exclude(shares_following_xn=None)\
            .values_list('shares_following_xn',
                         'adjustment_factor',
                         'conversion_price')

        if sec_obj.deriv_or_nonderiv == 'D' and\
                len(units_held_and_adj_and_conv_vectors) > 0:
            weighted_avg_conversion = \
                calc_weighted_avg_conversion(
                    units_held_and_adj_and_conv_vectors)
        else:
            weighted_avg_conversion = None

        if sec_obj.deriv_or_nonderiv == 'D' and\
                len(units_held_and_adj_and_conv_vectors) > 0:
            conv_vector =\
                Form345Entry.objects.filter(supersededdt=None)\
                .exclude(shares_following_xn=0)\
                .exclude(shares_following_xn=None)\
                .filter(security_id=security_id)\
                .values_list('conversion_price', flat=True)
            min_conversion_price = min(conv_vector)
            max_conversion_price = max(conv_vector)
        else:
            min_conversion_price = None
            max_conversion_price = None
        # Underlying shares total
        if sec_obj.deriv_or_nonderiv == 'D' and\
                latest_transaction.underlying_security is not None:
            underlying_shares_total = \
                latest_transaction.underlying_security.conversion_multiple *\
                units_held
        else:
            underlying_shares_total = None

# FOR CHECKING IN CASE OF ERROR
        # print 'sec_obj.issuer', sec_obj.issuer
        # print 'sec_obj.short_sec_title', sec_obj.short_sec_title
        # print 'sec_obj.ticker', sec_obj.ticker
        # print 'units_held', units_held
        # print 'sec_obj.deriv_or_nonderiv', sec_obj.deriv_or_nonderiv
        # print 'first_expiration_date', first_expiration_date
        # print 'last_expiration_date', last_expiration_date
        # print 'wavg_exp_date', wavg_exp_date
        # print 'min_conversion_price', min_conversion_price
        # print 'max_conversion_price', max_conversion_price
        # print 'weighted_avg_conversion', weighted_avg_conversion
        # print 'sec_obj.scrubbed_underlying_title', \
            # sec_obj.scrubbed_underlying_title
        # print 'underlying_ticker', underlying_ticker
        # print 'underlying_shares_total', underlying_shares_total
        # print 'intrinsic_value', intrinsic_value
        # print 'first_transaction_date', first_transaction_date
        # print 'last_transaction_date', last_transaction_date
        # print ''
        # print ''

        security_view_object =\
            SecurityView(issuer=sec_obj.issuer,
                         security_id=security_id,
                         short_sec_title=sec_obj.short_sec_title,
                         ticker=sec_obj.ticker,
                         last_close_price=last_close_price,
                         units_held=units_held,
                         deriv_or_nonderiv=sec_obj.deriv_or_nonderiv,
                         first_expiration_date=first_expiration_date,
                         last_expiration_date=last_expiration_date,
                         wavg_expiration_date=wavg_exp_date,
                         min_conversion_price=min_conversion_price,
                         max_conversion_price=max_conversion_price,
                         wavg_conversion=weighted_avg_conversion,
                         scrubbed_underlying_title=
                         sec_obj.scrubbed_underlying_title,
                         underlying_ticker=underlying_ticker,
                         underlying_shares_total=underlying_shares_total,
                         underlying_close_price=underlying_close_price,
                         intrinsic_value=intrinsic_value,
                         first_xn=first_transaction_date,
                         most_recent_xn=last_transaction_date)

        security_view_objects.append(security_view_object)
    print 'deleting old...',
    SecurityView.objects.all().delete()
    print 'saving...',
    SecurityView.objects.bulk_create(security_view_objects)
    print 'done.'


def build_security_views_by_affiliation():
    print 'Building PersonHoldingView objects'
    print '    Sorting and linking...',
    person_holding_view_objects = []
    security_ids_and_affiliations = Form345Entry.objects\
        .filter(supersededdt=None)\
        .values_list('security', 'affiliation').distinct()
    for security_id, affiliation in security_ids_and_affiliations:
        latest_transaction =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security=security_id)\
            .filter(affiliation=affiliation)\
            .latest('filedatetime')
        if latest_transaction.underlying_security is not None:
            underlying_ticker = latest_transaction.underlying_security.ticker
        else:
            underlying_ticker = None
        sec_obj = Security.objects.get(pk=security_id)
        today = datetime.date.today()
        # expiration date searches / calculations
        # Maybe check this to set None expiration date to far in future
        expiration_date_unit_list =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .filter(affiliation=affiliation)\
            .exclude(expiration_date__lte=today)\
            .exclude(expiration_date=None)\
            .exclude(shares_following_xn=0)\
            .exclude(shares_following_xn=None)\
            .values_list('expiration_date',
                         'underlying_shares',
                         'adjustment_factor')
        if len(expiration_date_unit_list) > 0:
            wavg_exp_date = wavgdate(expiration_date_unit_list)
            expdatevector, expunit_vector, adjustment_vector = \
                zip(*expiration_date_unit_list)
            first_expiration_date = min(expdatevector)
            last_expiration_date = max(expdatevector)
        else:
            wavg_exp_date = None
            first_expiration_date = None
            last_expiration_date = None
        # transaction price searches / calculations
        xndatevector =\
            Form345Entry.objects\
            .filter(security_id=security_id)\
            .filter(supersededdt=None)\
            .filter(affiliation=affiliation)\
            .exclude(transaction_date=None)\
            .values_list('transaction_date', flat=True)
        if len(xndatevector) > 0:
            first_transaction_date = min(xndatevector)
            last_transaction_date = max(xndatevector)
        else:
            first_transaction_date = None
            last_transaction_date = None

        # units held calculation (adjusted for splits)
        units_held_and_adjustment_vectors =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .filter(affiliation=affiliation)\
            .exclude(shares_following_xn=None)\
            .exclude(shares_following_xn=0)\
            .exclude(adjustment_factor=None)\
            .values_list('shares_following_xn',
                         'adjustment_factor')
        if len(units_held_and_adjustment_vectors) == 0:
            units_held = 0
        elif len(units_held_and_adjustment_vectors) == 1:
            units_held = \
                units_held_and_adjustment_vectors[0][0] *\
                units_held_and_adjustment_vectors[0][1]
        else:
            dotproduct = sum(p * q for p, q in
                             units_held_and_adjustment_vectors)
            units_held = dotproduct

        if sec_obj.deriv_or_nonderiv == 'N' and\
                sec_obj.ticker is not None:
            price = \
                ClosePrice.objects\
                .filter(securitypricehist__security_id=security_id)\
                .latest('close_date').adj_close_price
            intrinsic_value =\
                units_held * price
            last_close_price = price
            underlying_close_price = None
        elif sec_obj.deriv_or_nonderiv == 'D' and\
                underlying_ticker is not None:
            # print security_id
            units_held_and_adj_and_conv_vectors =\
                Form345Entry.objects.filter(supersededdt=None)\
                .filter(security_id=security_id)\
                .filter(affiliation=affiliation)\
                .values_list('shares_following_xn',
                             'adjustment_factor',
                             'conversion_price')

            underlyingprice = \
                ClosePrice.objects\
                .filter(securitypricehist__security_id=
                        latest_transaction.underlying_security)\
                .latest('close_date').adj_close_price
            intrinsic_value =\
                intrinsicvalcalc(units_held_and_adj_and_conv_vectors,
                                 sec_obj.conversion_multiple,
                                 underlyingprice)
            last_close_price = None
            underlying_close_price = underlyingprice
        else:
            intrinsic_value = None
            last_close_price = None
            underlying_close_price = None

        weighted_avg_conversion = None
        min_conversion_price = None
        max_conversion_price = None
        units_held_and_adj_and_conv_vectors =\
            Form345Entry.objects.filter(supersededdt=None)\
            .filter(security_id=security_id)\
            .filter(affiliation=affiliation)\
            .exclude(shares_following_xn=0)\
            .exclude(shares_following_xn=None)\
            .values_list('shares_following_xn',
                         'adjustment_factor',
                         'conversion_price')

        if sec_obj.deriv_or_nonderiv == 'D' and\
                len(units_held_and_adj_and_conv_vectors) > 0:
            weighted_avg_conversion = \
                calc_weighted_avg_conversion(
                    units_held_and_adj_and_conv_vectors)
        else:
            weighted_avg_conversion = None

        if sec_obj.deriv_or_nonderiv == 'D' and\
                len(units_held_and_adj_and_conv_vectors) > 0:
            conv_vector =\
                Form345Entry.objects.filter(supersededdt=None)\
                .filter(security_id=security_id)\
                .filter(affiliation=affiliation)\
                .exclude(shares_following_xn=0)\
                .exclude(shares_following_xn=None)\
                .values_list('conversion_price', flat=True)
            min_conversion_price = min(conv_vector)
            max_conversion_price = max(conv_vector)
        else:
            min_conversion_price = None
            max_conversion_price = None
        # Underlying shares total
        if sec_obj.deriv_or_nonderiv == 'D' and\
                latest_transaction.underlying_security is not None:
            underlying_shares_total = \
                latest_transaction.underlying_security.conversion_multiple *\
                units_held
        else:
            underlying_shares_total = None
        affiliation_obj = Affiliation.objects.get(id=affiliation)
        owner = affiliation_obj.reporting_owner
        person_name = affiliation_obj.person_name
        person_title = latest_transaction.reporting_owner_title

# FOR CHECKING IN CASE OF ERROR
        # print 'sec_obj.issuer', sec_obj.issuer
        # print 'sec_obj.short_sec_title', sec_obj.short_sec_title
        # print 'sec_obj.ticker', sec_obj.ticker
        # print 'units_held', units_held
        # print 'sec_obj.deriv_or_nonderiv', sec_obj.deriv_or_nonderiv
        # print 'first_expiration_date', first_expiration_date
        # print 'last_expiration_date', last_expiration_date
        # print 'wavg_exp_date', wavg_exp_date
        # print 'min_conversion_price', min_conversion_price
        # print 'max_conversion_price', max_conversion_price
        # print 'weighted_avg_conversion', weighted_avg_conversion
        # print 'sec_obj.scrubbed_underlying_title', \
            # sec_obj.scrubbed_underlying_title
        # print 'underlying_ticker', underlying_ticker
        # print 'underlying_shares_total', underlying_shares_total
        # print 'intrinsic_value', intrinsic_value
        # print 'first_transaction_date', first_transaction_date
        # print 'last_transaction_date', last_transaction_date
        # print ''
        # print ''

        person_holding_view_object =\
            PersonHoldingView(issuer=sec_obj.issuer,
                              owner=owner,
                              person_name=person_name,
                              person_title=person_title,
                              security_id=security_id,
                              affiliation=affiliation_obj,
                              short_sec_title=sec_obj.short_sec_title,
                              ticker=sec_obj.ticker,
                              last_close_price=last_close_price,
                              units_held=units_held,
                              deriv_or_nonderiv=sec_obj.deriv_or_nonderiv,
                              first_expiration_date=first_expiration_date,
                              last_expiration_date=last_expiration_date,
                              wavg_expiration_date=wavg_exp_date,
                              min_conversion_price=min_conversion_price,
                              max_conversion_price=max_conversion_price,
                              wavg_conversion=weighted_avg_conversion,
                              scrubbed_underlying_title=
                              sec_obj.scrubbed_underlying_title,
                              underlying_ticker=underlying_ticker,
                              underlying_shares_total=underlying_shares_total,
                              underlying_close_price=underlying_close_price,
                              intrinsic_value=intrinsic_value,
                              first_xn=first_transaction_date,
                              most_recent_xn=last_transaction_date)

        person_holding_view_objects.append(person_holding_view_object)
    print 'deleting old...',
    PersonHoldingView.objects.all().delete()
    print 'saving...',
    PersonHoldingView.objects.bulk_create(person_holding_view_objects)
    print 'done.'


build_security_views()
build_security_views_by_affiliation()
