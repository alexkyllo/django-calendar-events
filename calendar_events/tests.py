from django.test import TestCase
from models import *
import json

# Create your tests here.
class TestEvents(TestCase):
    fixtures = ['django_calendar_events/calendar_events/fixtures.json']
    def setUp(self):
        pass

    def test_event_to_fullcalendar(self):
        e = Event.objects.get(pk=1)
        event_from_json = json.loads('{"start": "2014-08-30T00:10:52+00:00", "allDay": false, "end": "2014-08-30T01:10:43.548908+00:00", "id": 1, "title": "Test Event"}')
        self.assertEqual(event_from_json, e.to_fullcalendar())