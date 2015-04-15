from sdapp.models import ReportingPersonAtts


def convert_180_day_to_annual_perf(pf_180):
    pf_annual = (float(pf_180) + 1.0)**(365.0/180.0) - 1.0
    pf_annual_rounded = round(pf_annual * 100.0, 2)
    return str(pf_annual_rounded) + '%'


def convert_to_annual_perf(pf, days):
    pf_annual = (float(pf) + 1.0)**(365.0/float(days)) - 1.0
    pf_annual_rounded = round(pf_annual * 100.0, 2)
    return str(pf_annual_rounded) + '%'


def p_cat_perf(queryset, column_name, days):
    b = queryset.values_list(column_name, flat=True)
    performance = convert_to_annual_perf(sum(b) / len(b), days)
    return performance, len(b)


def t_cat_perf(queryset, column_name, days):
    b = queryset.values_list(column_name, 'buys')
    b_perf_sum = 0
    b_perf_len = 0
    for b_perf, buys in b:
        b_perf_sum += b_perf * buys
        b_perf_len += buys
    performance = convert_to_annual_perf(b_perf_sum / b_perf_len, days)
    return performance, b_perf_len


def p_set_test(a):
    print '10 days: ', p_cat_perf(a, 'b_perf_10', 10)
    print '30 days: ', p_cat_perf(a, 'b_perf_30', 30)
    print '60 days: ', p_cat_perf(a, 'b_perf_60', 60)
    print '90 days: ', p_cat_perf(a, 'b_perf_90', 90)
    print '120 days:', p_cat_perf(a, 'b_perf_120', 120)
    print '150 days:', p_cat_perf(a, 'b_perf_150', 150)
    print '180 days:', p_cat_perf(a, 'b_perf', 180)


def t_set_test(a):
    print '10 days: ', t_cat_perf(a, 'b_perf_10', 10)
    print '30 days: ', t_cat_perf(a, 'b_perf_30', 30)
    print '60 days: ', t_cat_perf(a, 'b_perf_60', 60)
    print '90 days: ', t_cat_perf(a, 'b_perf_90', 90)
    print '120 days:', t_cat_perf(a, 'b_perf_120', 120)
    print '150 days:', t_cat_perf(a, 'b_perf_150', 150)
    print '180 days:', t_cat_perf(a, 'b_perf', 180)


print 'BUYING performance evaluated by PERSON (perf, transactions)'
print 'activity_threshold == True'
a = ReportingPersonAtts.objects.filter(activity_threshold=True)\
    .exclude(b_perf=None)
p_set_test(a)
print ''
print 'all persons, irrespective of activity_threshold'
a = ReportingPersonAtts.objects.exclude(b_perf=None)
p_set_test(a)
print ''
print ''
print 'BUYING performance evaluated by TRANSACTION (perf, transactions)'
print 'activity_threshold == True'
a = ReportingPersonAtts.objects.filter(activity_threshold=True)\
    .exclude(b_perf=None)
t_set_test(a)
print ''
print 'all persons, irrespective of activity_threshold'
a = ReportingPersonAtts.objects.exclude(b_perf=None)
t_set_test(a)
