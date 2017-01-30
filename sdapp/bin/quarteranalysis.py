# import datetime
# from decimal import Decimal
# import pytz
# import sys
#
# import django.db
# from django.db.models import F, Q, Sum
#
# from sdapp.models import (Affiliation, DiscretionaryXnEvent, Form345Entry,
#                           PersonSignal, SecurityPriceHist, ClosePrice,
#                           SigDisplay, WatchedName)
#
#
# from sdapp.bin.globals import (abs_sig_min, big_xn_amt, buy,
#                                buy_response_to_perf, date_of_any_new_filings,
#                                perf_period_days_td, rel_sig_min,
#                                recent_sale_period, sell,
#                                sell_response_to_perf,
#                                seller, signal_detect_lookback,
#                                significant_stock_move, hist_sale_period,
#                                today, todaymid)
#
# from sdapp.bin.sdapptools import calc_perf

from sdapp.models import Form345Entry
import quandl

from django.conf import settings


settings.QUANDL_API_KEY

quandl.ApiConfig.api_key = settings.QUANDL_API_KEY
# placeholder until multiple codes loaded from list
ticker = 'MSFT'
code = 'ZES/' + ticker

quandl.get(code)
