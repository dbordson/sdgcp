from sdapp.models import SplitOrAdjustmentEvent, Form345Entry, Security
import datetime


def populate_forms_with_split_adjustments()

    split_adj_list = SplitOrAdjustmentEvent.objects\
        .filter(security=security_id)\
        .values_list('event_date', 'adjustment_factor')