from django.conf.urls import patterns, url
from django.views.generic import ListView
from sdapp.models import CompanyStockHist
from sdapp.views import options, pricedetail, formentrydetail,\
    affiliationdetail, holdingdetail


urlpatterns = \
    patterns('',
             url(r'^$',
                 ListView.as_view(
                     queryset=CompanyStockHist.objects.order_by('-ticker_sym'),
                     context_object_name='ticker_sym_avail',
                     template_name='sdapp/index.html')),
             url(r'^(?P<ticker_sym>\w+)/$', options, name='options'),
             url(r'^(?P<ticker_sym>\w+)/stockhist$', pricedetail,
                 name='pricedetail'),
             url(r'^(?P<ticker_sym>\w+)/formentries$', formentrydetail,
                 name='formentrydetail'),
             url(r'^(?P<ticker_sym>\w+)/affiliations$', affiliationdetail,
                 name='formentrydetail'),
             url(r'^(?P<ticker_sym>\w+)/holdings$', holdingdetail,
                 name='formentrydetail'),
             url(r'^(?P<ticker_sym>\w+)/holdings$', holdingdetail,
                 name='formentrydetail'),
             )
