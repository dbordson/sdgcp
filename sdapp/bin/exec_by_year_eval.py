from sdapp.models import YearlyReportingPersonAtts


def convert_to_annual_perf(pf, days):
    pf_annual = (float(pf) + 1.0)**(365.0/float(days)) - 1.0
    pf_annual_rounded = round(pf_annual * 100.0, 2)
    return str(pf_annual_rounded) + '%'


def p_cat_perf(queryset, year, perf_periods, horizons):
    year_perfs = []
    for perf_period in perf_periods:
        qs = queryset.filter(year=year)\
            .values_list(perf_period, flat=True)
        b = [x for x in qs if x is not None]
        days = horizons[perf_period]
        if len(b) != 0:
            perf_for_period = convert_to_annual_perf(sum(b) / len(b), days)
        else:
            perf_for_period = None
            b = []
        year_perfs.append(perf_for_period)
    return len(b), year_perfs


def t_cat_perf(queryset, year, perf_periods, horizons):
    year_perfs = []
    for perf_period in perf_periods:
        qs = queryset.filter(year=year)\
            .values_list(perf_period, 'buys')
        b = [(x, y) for (x, y) in qs if x is not None and y is not None]
        if len(b) != 0:
            b_perf_sum = 0
            b_perf_len = 0

            for b_perf, buys in b:
                b_perf_sum += b_perf * buys
                b_perf_len += buys
            days = horizons[perf_period]
            perf_for_period =\
                convert_to_annual_perf(b_perf_sum / b_perf_len, days)
        else:
            perf_for_period = None
            b_perf_len = 0
        year_perfs.append(perf_for_period)
    return b_perf_len, year_perfs


def p_set_test(a, years, perf_periods, horizons):
    print 'Annualized performance by filing year and performance horizon'
    print 'Year | b_perf_10 | b_perf_30 | b_perf_60 | b_perf_90 | b_perf_120',
    print '| b_perf_150 | b_perf_180'

    for year in years:
        print 'Year:', year, p_cat_perf(a, year, perf_periods, horizons)
    print ''
    print ''
    return


def t_set_test(a, years, perf_periods, horizons):
    print 'Annualized performance by filing year and performance horizon'
    print 'Year | b_perf_10 | b_perf_30 | b_perf_60 | b_perf_90 | b_perf_120',
    print '| b_perf_150 | b_perf_180'

    for year in years:
        print 'Year:', year, t_cat_perf(a, year, perf_periods, horizons)


def review_years(years):
    perf_periods = ['b_perf_10', 'b_perf_30', 'b_perf_60', 'b_perf_90',
                    'b_perf_120', 'b_perf_150', 'b_perf_180']
    horizons =\
        {'b_perf_10': 10, 'b_perf_30': 30, 'b_perf_60': 60, 'b_perf_90': 90,
         'b_perf_120': 120, 'b_perf_150': 150, 'b_perf_180': 180}
    print 'BUYING performance evaluated by PERSON (perf, transactions)'
    print 'all persons, irrespective of activity_threshold'
    a = YearlyReportingPersonAtts.objects.all()
    p_set_test(a, years, perf_periods, horizons)
    print ''
    print ''
    print 'BUYING performance evaluated by TRANSACTION (perf, transactions)'
    print 'all persons, irrespective of activity_threshold'
    a = YearlyReportingPersonAtts.objects.all()
    t_set_test(a, years, perf_periods, horizons)

years =\
    YearlyReportingPersonAtts.objects.order_by('year')\
    .values_list('year', flat=True).distinct()

review_years(years)
