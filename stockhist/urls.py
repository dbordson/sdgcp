from django.conf.urls import patterns, url
from django.views.generic import ListView
from stockhist.models import CompanyStockHist
from stockhist.views import detail


urlpatterns = \
    patterns('',
             url(r'^$',
                 ListView.as_view(
                     queryset=CompanyStockHist.objects.order_by('-ticker_sym'),
                     context_object_name='ticker_sym_avail',
                     template_name='stockhist/index.html')),
             url(r'^(?P<ticker_sym>\w+)/$', detail, name='detail'),
             )
