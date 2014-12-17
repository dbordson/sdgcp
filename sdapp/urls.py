from django.conf.urls import patterns, url
from django.views.generic import ListView
from sdapp.models import Security
from sdapp.views import options, formentrydetail,\
    holdingdetail, byperson, holdingtable, personholdingtable


urlpatterns = \
    patterns(
        '',
        url(r'^$',
            ListView.as_view(
                queryset=Security.objects.exclude(ticker=None)
                .order_by('-ticker'),
                context_object_name='ticker_avail',
                template_name='sdapp/index.html')),
        url(r'^(?P<ticker>\w+)/$', options, name='options'),
        url(r'^(?P<ticker>\w+)/formentries$', formentrydetail,
            name='formentrydetail'),
        url(r'^(?P<ticker>\w+)/holdings$', holdingdetail,
            name='formentrydetail'),
        url(r'^(?P<ticker>\w+)/byperson$', byperson,
            name='byperson'),
        url(r'^(?P<ticker>\w+)/holdingtable$', holdingtable,
            name='holdingtable'),
        url(r'^(?P<ticker>\w+)/(?P<owner>\w+)/byperson$',
            personholdingtable,
            name='personholdingtable'),
        )
