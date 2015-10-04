import datetime
import pytz
from decimal import Decimal

signal_detect_lookback = datetime.timedelta(-180)
significant_stock_move = Decimal(.2)
abs_holding_min = Decimal(10000)
rel_holding_min = Decimal(.1)
perf_period_days = datetime.timedelta(-90)
EST = pytz.timezone('America/New_York')
today = today = datetime.date.today()
todaymid = datetime.datetime(today.year, today.month, today.day + 1,
                             0, 0, 0, 0, tzinfo=EST)

# Signal names
buy = "Buy"
buy_response_to_perf = "Buy Responsive to Performance"
sell = "Sell Responsive to Performance"
sell_response_to_perf = "Sell"
