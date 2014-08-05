from django.conf.urls import patterns, include, url
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', show_calendar, name="show_calendar"),
    url(r'^events/$', view_all_events_between, name="view_all_events_between"),
)
