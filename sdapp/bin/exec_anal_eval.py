from sdapp.models import ReportingPersonAtts


def convert_180_day_to_annual_perf(pf_180):
    pf_annual = (float(pf_180) + 1.0)**(365.0/180.0) - 1.0
    pf_annual_rounded = round(pf_annual * 100.0, 2)
    return str(pf_annual_rounded) + '%'


print 'Evaluated by person'

a = ReportingPersonAtts.objects.filter(activity_threshold=True)\
    .exclude(b_perf=None)
b = a.values_list('b_perf', flat=True)
performance = convert_180_day_to_annual_perf(sum(b) / len(b))
print 'Performance by persons with activity_threshold == True:', performance,
print 'Number of transactions:', len(b)

a = ReportingPersonAtts.objects.exclude(b_perf=None)
b = a.values_list('b_perf', flat=True)
performance = convert_180_day_to_annual_perf(sum(b) / len(b))
print 'Performance by all relevant persons:', performance
print 'Number of transactions:', len(b)
print ''
print 'Evaluated by transaction'
b_perf_sum = 0
b_perf_len = 0
a = ReportingPersonAtts.objects.filter(activity_threshold=True)\
    .exclude(b_perf=None)
b = a.values_list('b_perf', 'buys')
for b_perf, buys in b:
    b_perf_sum += b_perf * buys
    b_perf_len += buys
print 'Performance by transaction with activity_threshold == True:',
print convert_180_day_to_annual_perf(b_perf_sum / b_perf_len),
print 'Number of transactions:', b_perf_len

b_perf_sum = 0
b_perf_len = 0
a = ReportingPersonAtts.objects.exclude(b_perf=None)
b = a.values_list('b_perf', 'buys')
for b_perf, buys in b:
    b_perf_sum += b_perf * buys
    b_perf_len += buys
print 'Performance by all relevant transactions:',
print convert_180_day_to_annual_perf(b_perf_sum / b_perf_len),
print 'Number of transactions:', b_perf_len
