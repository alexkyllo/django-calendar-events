from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.

def show_calendar(request, *args, **kwargs):
	return render_to_response('show_calendar.html', context_instance=RequestContext(request))
