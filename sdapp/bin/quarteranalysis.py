import pandas
import quandl
import sys
# See https://www.quandl.com/data/ZES-Consensus-Earnings-Surprises for info.

from django.conf import settings
from django.db.models import Q, Sum

from sdapp.bin.globals import earnings_transaction_lookback, EST
from sdapp.bin.sdapptools import rep_none_with_zero
from sdapp.models import Form345Entry, SecurityPriceHist


def append_df(df1, df2):
    if df1 is None:
        return df2
    else:
        return pandas.concat([df1, df2])


def assemble_ticker_dataframe(ticker):
    code = 'ZES/' + ticker
    sph = SecurityPriceHist.objects.filter(ticker_sym=ticker).first()
    # Set up blank pandas dataframe for insider info
    workdf = pandas.DataFrame({
        'purch_disc': [], 'sale_disc': [],
        'purch_disc_ceo': [], 'sale_disc_ceo': [],
        'purch_disc_no_10b5': [], 'sale_disc_no_10b5': [],
        'purch_disc_ceo_no_10b5': [], 'sale_disc_ceo_no_10b5': []})
    if sph is None:
        # This means there is no match to the quandl ticker in our DB.
        print 'No issuer record for ticker:', ticker
        return None
    else:
        issuer = sph.issuer
    #
    # Here we pull down the quandl data
    basedf = quandl.get(code)
    # Select the quandl columns we care about
    selected_quandl_df = basedf[[
        'EPS_MEAN_EST', 'EPS_ACT', 'EPS_AMT_DIFF_SURP',
        'EPS_PCT_DIFF_SURP', 'EPS_STD_EST', 'EPS_CNT_EST']]
    #
    for index, row in basedf.iterrows():
        # Here we use the issuer and quandl data date to pull insider data
        # for a relevant period.
        index_datetime = index.to_datetime().replace(tzinfo=EST)
        lookback_datetime =\
            index_datetime.replace(tzinfo=EST) - earnings_transaction_lookback
        #
        # Query pulls all discretionary issuer transactions for the period.
        transactions = Form345Entry.objects\
            .filter(issuer_cik=issuer, filedatetime__gte=lookback_datetime,
                    filedatetime__lt=index_datetime)
        #
        # Calc purchase and sale values
        purch_disc = rep_none_with_zero(
            transactions.filter(transaction_code='P')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        sale_disc = rep_none_with_zero(
            transactions.filter(transaction_code='S')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        #
        # Calc purchase and sale values for CEO
        disc_ceo = transactions\
            .filter(is_officer=True)\
            .filter(
                Q(reporting_owner_title__icontains='ceo') |
                Q(reporting_owner_title__icontains='chief executive officer'))
        purch_disc_ceo = rep_none_with_zero(
            disc_ceo.filter(transaction_code='P')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        sale_disc_ceo = rep_none_with_zero(
            disc_ceo.filter(transaction_code='S')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        #
        # Calc purchase and sale values for non-10b5 transactions
        disc_no_10b5 = transactions.filter(tenbfive_note=None)
        purch_disc_no_10b5 = rep_none_with_zero(
            disc_no_10b5.filter(transaction_code='P')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        sale_disc_no_10b5 = rep_none_with_zero(
            disc_no_10b5.filter(transaction_code='S')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        #
        # Calc purchase and sale values for non-10b5 transactions for CEO
        disc_ceo_no_10b5 =\
            disc_ceo.filter(tenbfive_note=None)
        purch_disc_ceo_no_10b5 = rep_none_with_zero(
            disc_ceo_no_10b5.filter(transaction_code='P')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        sale_disc_ceo_no_10b5 = rep_none_with_zero(
            disc_ceo_no_10b5.filter(transaction_code='S')
            .aggregate(Sum('xn_value'))['xn_value__sum'])
        #
        # Add the insider data to a blank working dataframe
        workdf.loc[index] = \
            [purch_disc, sale_disc,
             purch_disc_ceo, sale_disc_ceo,
             purch_disc_no_10b5, sale_disc_no_10b5,
             purch_disc_ceo_no_10b5, sale_disc_ceo_no_10b5]
    #
    # Add our insider data to the selected quandl data
    ticker_df = pandas.concat([selected_quandl_df, workdf],
                              axis=1, join='inner')
    return ticker_df


def combine_quandl_and_insider_data():
    # Pull quandl api key from settings and log in
    settings.QUANDL_API_KEY
    quandl.ApiConfig.api_key = settings.QUANDL_API_KEY
    # placeholder until multiple codes loaded from list
    earnings_insider_df = None
    # This loop quickly measures the ticker file length for use in real
    # time progress counter.
    with open('quandlZESSampleNames.txt') as f:
        for i, l in enumerate(f):
            pass
    #
    count = 0.0
    looplength = i + 1
    with open('quandlZESSampleNames.txt') as infile:
        for line in infile:
            ticker = str(line.strip())
            # Process the ticker on this line of the file
            ticker_df = assemble_ticker_dataframe(ticker)
            if ticker_df is not None:
                # Add the current ticker to the master list
                earnings_insider_df =\
                    append_df(earnings_insider_df, ticker_df)
            # Counter
            count += 1.0
            percentcomplete = round(count / looplength * 100, 2)
            sys.stdout.write("\r%s / %s tickers: %.2f%%" %
                             (int(count), int(looplength),
                              percentcomplete))
            sys.stdout.flush()
    return earnings_insider_df
#
# ticker = 'MSFT'
#
# ticker_df = assemble_ticker_dataframe(ticker)
