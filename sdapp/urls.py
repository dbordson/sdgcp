from django.conf.urls import patterns, url
# from django.views.generic import ListView
# from sdapp.models import Security
from sdapp.views import (options, formentrydetail, screens, holdingdetail,
                         filterintermed, watchtoggle, index, tickersearch,
                         drilldown, searchsignals, watchlisttoggle)


urlpatterns = \
    patterns(
        '',
        url(r'^$', screens, name='screens'),
        url(r'^index', index, name='index'),
        url(r'^tickersearch/', tickersearch, name='tickersearch'),
        url(r'^watchtoggle/', watchtoggle, name='watchtoggle'),
        url(r'^filter-intermed/$', filterintermed, name='filterintermed'),
        url(r'^search/', searchsignals),
        url(r'^(?P<ticker>[^/]+)/$', options, name='options'),
        url(r'^(?P<ticker>[^/]+)/drilldown$', drilldown, name='drilldown'),
        url(r'^(?P<ticker>[^/]+)/bigchart$', drilldown, name='bigchart'),
        url(r'^(?P<ticker>[^/]+)/formentries$', formentrydetail,
            name='formentrydetail'),
        url(r'^(?P<ticker>[^/]+)/holdings$', holdingdetail,
            name='holdingdetail'),
        url(r'^(?P<ticker>[^/]+)/watchlisttoggle/', watchlisttoggle,
            name='watchlisttoggle'),
        )
