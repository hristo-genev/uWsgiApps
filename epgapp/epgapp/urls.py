from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
import epgapp.forms
import epgapp.views
from django.contrib import admin
#from django.contrib.auth import views as auth_views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', epgapp.views.ChannelListView.as_view(), name='channel-list'),
    url(r'^channel/(?P<slug>.+)/grab/$', epgapp.views.grab, name='grab'),
    url(r'^channel/(?P<slug>.+?)/$', epgapp.views.ChannelDetailView.as_view(), name='channel-detail'),
    url(r'^siteinis$', epgapp.views.SiteiniListView.as_view(), name='siteini-list'),
    #url(r'^test$', epgapp.views.siteini_test, name='siteini-test'),
    url(r'^test/(?P<slug>.*?)$', epgapp.views.siteini_test, name='siteini-test'),
    #url(r'^siteini/(?P<pk>.+?)/$', epgapp.views.SiteiniDetailView.as_view(), name='siteini-detail'),
    url(r'^siteini/(?P<slug>.+?)/$', epgapp.views.SiteiniDetailView.as_view(), name='siteini-detail'),
    url(r'^contact$', epgapp.views.contact, name='contact'),
    url(r'^grabbing/run/all/(?P<id>.+?)$', epgapp.views.run, name='run'),
    url(r'^grabbing/run/test$', epgapp.views.run_siteini_test, name='run-siteini-test'),
    url(r'^grabbing/epg/log/(?P<siteini>.+)$', epgapp.views.get_epg_log, name='get-epg-log'),
    url(r'^grabbing/epg/raw/(?P<siteini>.+)$', epgapp.views.get_siteini_epg, name='get-siteini-epg-raw'),
    url(r'^grabbing/epg/report$', epgapp.views.get_epg_report, name='get-epg-report'),
    url(r'^grabbing/epg/download$', epgapp.views.epg_download, name='epg-download'),
    url(r'^stats/$', epgapp.views.stats, name='stats-url'),
    url(r'^grabbing/run/status/(?P<processId>.+)$', epgapp.views.status, name='status'),
    url(r'^grabbing$', epgapp.views.grabbing, name='grabbing'),
    url(r'^login/$', django.contrib.auth.views.LoginView.as_view(), name='login'),
    url(r'^logout$', django.contrib.auth.views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^settings/*$', epgapp.views.settings, name='settings-url'),
    url(r'^settings/raw/(?P<id>.+?)$', epgapp.views.exported_settings, name='exported-settings'),
    url(r'^settings/raw/$', epgapp.views.exported_settings, name='exported-last-settings')
]