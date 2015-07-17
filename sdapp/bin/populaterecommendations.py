from sdapp.models import Signal, Recommendation
import datetime
import pytz
from decimal import Decimal


print 'Populating Recommendation objects...'


# This recommendation script is really subjective.
# As it stands, we have a few moving parts.  We may want to do analysis to
# vet the assumptions.  I assume that recommendation confidence should be
# based on three factors: (1) signal type [certain signals are stronger than
# others], (2) the dollar value of the transaction underlying the signal and
# (3) how recent the signal was.

today = datetime.datetime.now(pytz.utc)
confident_lookback_days = datetime.timedelta(-30)

issuer_ids_with_signals =\
    Signal.objects.values_list('issuer', flat=True).distinct()
recommendation_objects_to_add = []

for issuer_id in issuer_ids_with_signals:
    issuer_signals =\
        Signal.objects.filter(issuer=issuer_id).order_by('-signal_date')
    positive_signals =\
        ['Discretionary Buy after a Decline', 'Discretionary Buy']
    # negative_signals = []
    signal_count = Decimal(0)
    net_signal = Decimal(0)
    for issuer_signal in issuer_signals:
        signal_count += Decimal(1)
        if issuer_signal.signal_name in positive_signals:
            net_signal += Decimal(1)
    pos_signal_rate = net_signal / signal_count
    if issuer_signals[0].signal_name in positive_signals:
        latest_signal_positive = True
    else:
        latest_signal_positive = False
    if pos_signal_rate > Decimal(.7) and latest_signal_positive:
        sentiment = 'Bullish'
        if pos_signal_rate > Decimal(.85) and signal_count > 1:
            confidence = 'Strong'
        elif pos_signal_rate > Decimal(.85):
            confidence = 'Moderate'
        else:
            confidence = 'Weak'

    if pos_signal_rate < Decimal(.3) and not latest_signal_positive:
        sentiment = 'Bearish'
        if pos_signal_rate < Decimal(.15) and signal_count > 1:
            confidence = 'Strong'
        elif pos_signal_rate < Decimal(.15):
            confidence = 'Moderate'
        else:
            confidence = 'Weak'

    recommendation_object =\
        Recommendation(issuer_id=issuer_id,
                       sentiment=sentiment,
                       confidence=confidence)
    recommendation_objects_to_add.append(recommendation_object)

print 'deleting old recommendations...'
Recommendation.objects.all().delete()
print 'adding new recommendations...'
Recommendation.objects.bulk_create(recommendation_objects_to_add)
print 'done.'
