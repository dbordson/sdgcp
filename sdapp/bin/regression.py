import pandas
a = TransactionEvent.objects.all().values_list()
b = zip(*a)


df = pandas.DataFrame(list(BlogPost.objects.all().values()))


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