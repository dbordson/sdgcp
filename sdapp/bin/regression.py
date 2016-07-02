from sdapp.models import TransactionEvent
import pandas as pd
import statsmodels.api as sm
import numpy as np
# Try to take numpy out of this.  The package is not otherwise used.
# Perhaps there is another NaN definition in pandas?


def fl(x):
    try:
        a = float(x)
    except:
        a = np.nan
    return a


df = TransactionEvent.objects.all().values_list()


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

# result = sm.OLS(df['perf_at_91_days'], df['net_xn_pct'])
# # result = sm.ols(formula="A ~ B + C", data=df).fit()
# result = s
