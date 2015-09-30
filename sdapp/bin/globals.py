import datetime
from decimal import Decimal

lookback = datetime.timedelta(-180)
weakness_drop = Decimal(.2)
abs_significance_minimum = Decimal(10000)
rel_significance_minimum = Decimal(.1)
