from django.conf.urls import patterns, include, url
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', show_calendar, name="show_calendar"),
    url(r'^events/$', view_all_events_between, name="view_all_events_between"),
    url(r'^events/list/$', EventList.as_view(), name="event_list"),
    url(r'^events/create/$', EventCreate.as_view(success_url='/calendar/'), name="event_create"),
    url(r'^events/(?P<pk>\d+)/update/$', EventUpdate.as_view(success_url='/calendar/'), name="event_update"),
    url(r'^events/(?P<pk>\d+)/delete/$', EventDelete.as_view(success_url='/calendar/'), name="event_delete"),
)
