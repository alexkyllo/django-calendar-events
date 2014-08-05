from django.shortcuts import render, render_to_response
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from models import *
from dateutil import parser
import json

# Create your views here.

def show_calendar(request, *args, **kwargs):
    return render_to_response('show_calendar.html', context_instance=RequestContext(request))

@require_GET
def view_all_events_between(request, **kwargs):
    '''
    This view is for the jquery-ui fullcalendar widget. Takes a GET request with a date range and returns all events inside the range
    in the JSON format that fullcalendar is expecting.
    '''
   
    startdatetime = parser.parse(request.GET['start']+'T00:00:00.0+00:00')
    enddatetime = parser.parse(request.GET['end']+'T00:00:00.0+00:00')
    event_occurrences = Event.get_event_occurrences_static(startdatetime,enddatetime)
    
    if event_occurrences is None:
        return HttpResponse("[]")
    else:
        fullcalendar_events = [occurrence.to_fullcalendar() for occurrence in event_occurrences]
        return HttpResponse(json.dumps(fullcalendar_events))