from django.shortcuts import render, render_to_response
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from models import *
from forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dateutil import parser
import json

# Create your views here.

def show_calendar(request, *args, **kwargs):
    return render_to_response('calendar_events/show_calendar.html', context_instance=RequestContext(request))

@require_GET
def view_all_events_between(request, **kwargs):
    '''
    This view is for the jquery-ui fullcalendar widget. Takes a GET request with a date range and returns all events inside the range
    in the JSON format that fullcalendar is expecting.
    '''
   
    startdatetime = parser.parse(request.GET['start']+'T00:00:00.0+00:00')
    enddatetime = parser.parse(request.GET['end']+'T00:00:00.0+00:00')
    events = Event.objects.all()
    event_occurrences = [event.get_occurrences(startdatetime,enddatetime) for event in events]
    
    if event_occurrences is None:
        return HttpResponse("[]")
    else:
        event_occurrences_flat = [item for sublist in event_occurrences for item in sublist] #flatten the list of lists of events
        fullcalendar_events = [occurrence.to_fullcalendar() for occurrence in event_occurrences_flat]
        return HttpResponse(json.dumps(fullcalendar_events))

class EventList(ListView):
    model = Event

#    def get_queryset(self):
#        return Event.objects.all()

class EventCreate(CreateView):
    model = Event
    form_class = EventForm

class EventDelete(DeleteView):
    model = Event

class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm

class EventDetail(DetailView):
    model = Event