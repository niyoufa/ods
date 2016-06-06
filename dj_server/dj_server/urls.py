#coding=utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

)

#/dhui/api/
urlpatterns += patterns('dhui.api_views',
    url(r'^%s/$' % settings.DHUI_URL_PREFIX,"api_router"),
)