from sdapp.models import TransactionEvent
import pandas as pd
import statsmodels.api as sm
import numpy as np

def fl(x):
    try:
        a = float(x)
    except:
        a = np.nan
    return a


df = TransactionEvent.objects.all().values_list()
b = zip(*a)


def regression(ystring, xstring):
    df =\
        pd.DataFrame(list(TransactionEvent.objects.all()
                     .values(ystring, xstring)))
    # df91 = df91.replace([None], np.nan)
    df = df[pd.notnull(df[ystring])]
    df = df[pd.notnull(df[xstring])]
    df['f_ystring'] = df[ystring].map(fl)
    df['f_xstring'] = df[xstring].map(fl)
    y = np.array(df.f_ystring)
    X = df.f_xstring
    X = np.array(sm.add_constant(X))
    est = sm.OLS(y, X)
    est = est.fit()
    print est.summary()
    return


ystring = 'perf_at_91_days'
xstring = 'net_xn_pct'
regression(ystring, xstring)

result = sm.OLS(df['perf_at_91_days'], df['net_xn_pct'])
# result = sm.ols(formula="A ~ B + C", data=df).fit()
result = s

# d = 'issuer':
#     'net_xn_val':
#     'end_holding_val':
#     'net_xn_pct':
#     'period_start':
#     'period_end':
#     'price_at_period_end':
#     'perf_at_91_days':
#     'perf_at_182_days':
#     'perf_at_274_days';
#     'perf_at_365_days':
#     'perf_at_456_days':