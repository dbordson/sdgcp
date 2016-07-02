import datetime
import pytz
from decimal import Decimal

# Below tracking period starts at beginning of calendar year
# that begins such that period begins as of 1/1/X, where
# X = current calendar year - tracking_period_calendar_years.
tracking_period_calendar_years = 5
signal_detect_lookback = datetime.timedelta(180)
recent_sale_period = datetime.timedelta(91)
hist_sale_period = datetime.timedelta(91 + 365)
grant_period_calc_lookback = datetime.timedelta(730)
min_day_gap_for_10b51_trigger_sell_rate = 10
price_trigger_lookback = datetime.timedelta(30)
trigger_min_stock_move = Decimal(.1000)
# Get rid of below at some point
significant_stock_move = Decimal(10)  # percent
abs_sig_min = Decimal(10 * 1000)
rel_sig_min = Decimal(.1)
perf_period_days_td = datetime.timedelta(90)
big_xn_amt = Decimal(100 * 1000)
EST = pytz.timezone('America/New_York')
now = datetime.datetime.now(EST)

UTC = pytz.timezone('UTC')
nowUTC = datetime.datetime.now(UTC)
# THIS TIME ASSUMES THE SCRIPT WILL NOT RUN BTW 2 am and 3 am EST
if now.time().hour >= 3:
    delta = datetime.timedelta(-1)
else:
    delta = datetime.timedelta(-2)
today = datetime.date.today()
# todaymid is midnight for the most recent filing index
todaymid = datetime.datetime(today.year, today.month, today.day,
                             0, 0, 0, 0, tzinfo=EST)\
    + datetime.timedelta(1)
date_of_any_new_filings = today + delta
# Person Signal names
buy = "Buy"
buy_response_to_perf = "Buy Responsive to Performance"
sell = "Sell"
sell_response_to_perf = "Sell Responsive to Performance"


# View global variables
sel_person_id = 'person_cik'

# Signal Display names
buy_on_weakness = "Buying in Response to Performance"
cluster_buy = "Cluster Buying"
discretionary_buy = "Plain Vanilla Buying"
sell_on_strength = "Selling in Response to Performance"
cluster_sell = "Cluster Selling"
discretionary_sell = "Plain Vanilla Selling"

signal_disp_list = \
    [buy_on_weakness, cluster_buy, discretionary_buy,
     sell_on_strength, cluster_sell, discretionary_sell]

# Affiliation behavior options
seller = "Seller"
buyer = "Buyer"

# quarterly index download options
# indexyear lookback is the lookback from the nominal current year
# e.g. 11 years looking back from 4/3/16 looks back to 1/1/2005.
indexyearlookback = 10

app_url = 'http://127.0.0.1:8000/sdapp/'
