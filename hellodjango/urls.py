from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
# import re


admin.autodiscover()

urlpatterns =\
    patterns('',
             url(r'^$', 'signups.views.home', name='home'),
             url(r'^thank-you/$', 'signups.views.thankyou', name='thankyou'),
             url(r'^duplicate/$',
                 'signups.views.duplicate_login', name='duplicate_login'),
             url(r'^about-us/$', 'signups.views.aboutus', name='aboutus'),
             # url(r'^blog/', include('blog.urls')),
             url(r'^accountinfo/$', 'hellodjango.views.accountinfo'),
             url(r'^changepw/$', 'hellodjango.views.changepw',
                 name='changepw'),
             url(r'^changepw/auth/$', 'hellodjango.views.changepwauth'),
             url(r'^accountinfo/watchlist/$',
                 'hellodjango.views.managewatchlist', name='managewatchlist'),
             url(r'^pwreminder/$', 'hellodjango.views.pwreminder'),
             url(r'^sdapp/', include('sdapp.urls')),
             url(r'^admin/', include(admin.site.urls)),

             # user auth urls
             url(r'^accounts/login/$', 'hellodjango.views.login'),
             url(r'^accounts/auth/$', 'hellodjango.views.auth_view'),
             url(r'^accounts/logout/$', 'hellodjango.views.logout',
                 name='logout'),
             url(r'^accounts/loggedin/$', 'hellodjango.views.loggedin'),
             url(r'^accounts/invalid/$', 'hellodjango.views.invalid_login'),
             )

urlpatterns += patterns('',
                        (r'^static/(.*)$', 'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT}),
                        )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL,
                          # document_root=settings.MEDIA_ROOT)
