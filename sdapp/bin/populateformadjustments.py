from sdapp.models import SplitOrAdjustmentEvent, Form345Entry, Security
import datetime
from operator import mul
from django.db import models


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


populate_stock_forms_with_split_adjustments()
populate_derivative_forms_with_split_adjustments()
