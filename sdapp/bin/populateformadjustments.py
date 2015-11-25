import datetime
from decimal import Decimal
import sys

# from operator import mul
from django.db import models

from sdapp.models import SplitOrAdjustmentEvent, Form345Entry, Security


def median(medlist):
    if len(medlist) == 0:
        return Decimal(1)
    medlist.sort()
    i = len(medlist)/2
    if len(medlist) % 2 == 0:
        median_number = (medlist[i] + medlist[i-1])/2
    else:
        median_number = medlist[i]
    return median_number


def populate_stock_forms_with_split_adjustments():
    print 'Checking for unadjusted stock Form345Entry objects...'
    latest_split_set =\
        set(SplitOrAdjustmentEvent.objects.values('security_id')
            .annotate(max_date=models.Max('event_date'))
            .values_list('max_date', 'security'))

    form_split_set =\
        set(Form345Entry.objects
            .exclude(security__splitoradjustmentevent=None)
            .exclude(security__ticker=None)
            .values_list('adjustment_date', 'security')
            .distinct())
    print '    Sorting...',
    forms_to_update =\
        form_split_set - (form_split_set & latest_split_set)

    print 'linking and saving...',
    for form_last_adjustment_date, security_id in forms_to_update:
        split_adj_factor_list = SplitOrAdjustmentEvent.objects\
            .filter(security=security_id)\
            .order_by('-event_date')\
            .values_list('adjustment_factor', 'event_date')
        adjustment_entries = [list(row) for row in split_adj_factor_list]
        # build date ranges to determine adjustment amounts
        adjustmentfactor = 1
        for index, row in enumerate(adjustment_entries):
            if adjustment_entries.index(row) == len(adjustment_entries) - 1:
                adjustmentfactor = adjustmentfactor * row[0]
                row[0] = adjustmentfactor
                row.append(datetime.date(1990, 1, 1))
            else:
                adjustmentfactor = adjustmentfactor * row[0]
                row[0] = adjustmentfactor
                row.append(adjustment_entries[index + 1][1])
        for adjust_factor, end_filter_date, start_filter_date in\
                adjustment_entries:
            Form345Entry.objects.filter(security=security_id)\
                .filter(adjustment_date=form_last_adjustment_date)\
                .filter(period_of_report__lt=end_filter_date)\
                .filter(period_of_report__gte=start_filter_date)\
                .update(**{'adjustment_factor': adjust_factor,
                           'adjustment_date': end_filter_date})
        Form345Entry.objects.filter(security=security_id)\
            .filter(adjustment_date=form_last_adjustment_date)\
            .filter(period_of_report__gte=adjustment_entries[0][1])\
            .update(**{'adjustment_factor': 1.0,
                       'adjustment_date': adjustment_entries[0][1]})

    print 'done.'


def populate_derivative_forms_with_split_adjustments():
    print 'Checking for unadjusted derivative Form345Entry objects...'
    latest_split_set =\
        set(SplitOrAdjustmentEvent.objects.values('security_id')
            .annotate(max_date=models.Max('event_date'))
            .values_list('max_date', 'security'))

    form_split_set =\
        set(Form345Entry.objects
            .exclude(underlying_security__splitoradjustmentevent=None)
            .exclude(underlying_security__ticker=None)
            .values_list('adjustment_date', 'underlying_security')
            .distinct())
    print '    Sorting...',
    forms_to_update =\
        form_split_set - (form_split_set & latest_split_set)

    print 'linking and saving...',
    for form_last_adjustment_date, underlying_security_id in forms_to_update:
        split_adj_factor_list = SplitOrAdjustmentEvent.objects\
            .filter(security=underlying_security_id)\
            .order_by('-event_date')\
            .values_list('adjustment_factor', 'event_date')
        adjustment_entries = [list(row) for row in split_adj_factor_list]
        # build date ranges to determine adjustment amounts
        adjustmentfactor = 1
        for index, row in enumerate(adjustment_entries):
            if adjustment_entries.index(row) == len(adjustment_entries) - 1:
                adjustmentfactor = adjustmentfactor * row[0]
                row[0] = adjustmentfactor
                row.append(datetime.date(1990, 1, 1))
            else:
                adjustmentfactor = adjustmentfactor * row[0]
                row[0] = adjustmentfactor
                row.append(adjustment_entries[index + 1][1])
        for adjust_factor, end_filter_date, start_filter_date in\
                adjustment_entries:
            Form345Entry.objects\
                .filter(underlying_security=underlying_security_id)\
                .filter(adjustment_date=form_last_adjustment_date)\
                .filter(period_of_report__lt=end_filter_date)\
                .filter(period_of_report__gte=start_filter_date)\
                .update(**{'adjustment_factor': adjust_factor,
                           'adjustment_date': end_filter_date})
        Form345Entry.objects\
            .filter(underlying_security=underlying_security_id)\
            .filter(adjustment_date=form_last_adjustment_date)\
            .filter(period_of_report__gte=adjustment_entries[0][1])\
            .update(**{'adjustment_factor': 1.0,
                       'adjustment_date': adjustment_entries[0][1]})

    print 'done.'


def populate_conversion_factors():
    print 'Replacing Security object conversion factors...'
    latest_conv_list = Form345Entry.objects.exclude(transaction_shares=None)\
        .filter(deriv_or_nonderiv='D')\
        .exclude(underlying_security__ticker=None)\
        .values_list('security_id', flat=True).distinct()
    looplength = float(len(latest_conv_list))
    counter = 0.0
    for security_id in latest_conv_list:
        sampleentries =\
            Form345Entry.objects.filter(security=security_id)\
            .exclude(underlying_shares=Decimal(0))\
            .exclude(transaction_shares=Decimal(0))\
            .exclude(underlying_shares=None)\
            .exclude(transaction_shares=None)\
            .order_by('filedatetime')[:10]\
            .values_list('underlying_shares', 'transaction_shares',
                         'adjustment_factor')
        conversion_multiples = [(p / q) * r for p, q, r in sampleentries]
        conversion_multiple = median(conversion_multiples)
        Security.objects.filter(id=security_id)\
            .update(conversion_multiple=conversion_multiple)
        counter += 1.0
        percentcomplete = round(counter / looplength * 100, 2)
        sys.stdout.write("\r%s / %s conversion factors to replace: %.2f%%" %
                         (int(counter), int(looplength), percentcomplete))
        sys.stdout.flush()
    print '\ndone.'


populate_stock_forms_with_split_adjustments()
populate_derivative_forms_with_split_adjustments()
populate_conversion_factors()
