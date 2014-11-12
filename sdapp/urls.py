from django.conf.urls import patterns, url
from django.views.generic import ListView
from sdapp.models import SecurityPriceHist
from sdapp.views import options, pricedetail, formentrydetail,\
    affiliationdetail, holdingdetail, holdingtable, individualaffiliation,\
    holdingtypes


urlpatterns = \
    patterns('',
             url(r'^$',
                 ListView.as_view(
                     queryset=SecurityPriceHist.objects.order_by('-ticker_sym'),
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
             url(r'^(?P<ticker_sym>\w+)/holdingtable$', holdingtable,
                 name='holdingtable'),
             url(r'^(?P<ticker_sym>\w+)/(?P<reporting_owner_cik_num>\w+)/holdingtypes$', holdingtypes,
                 name='holdingtypes'),
             url(r'^(?P<ticker_sym>\w+)/(?P<reporting_owner_cik_num>\w+)/affiliation$', individualaffiliation,
                 name='individualaffiliation'),
             )
