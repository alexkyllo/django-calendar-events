from django.test import TestCase
from models import *
from dateutil.rrule import *
import json

# Create your tests here.
class TestEvents(TestCase):
    fixtures = ['django_calendar_events/calendar_events/fixtures.json']
    def setUp(self):
        pass

    def test_event_to_fullcalendar(self):
        e = Event.objects.get(pk=1)
        event_from_json = json.loads('{"start": "2014-08-02T00:10:00+00:00", "allDay": false, "end": "2014-08-02T01:10:43.548908+00:00", "id": 1, "title": "Test Event", "url": "/calendar/events/1/"}')
        event_from_fullcalendar = e.to_fullcalendar()
        self.assertEqual(event_from_json['title'], event_from_fullcalendar['title'])

    def test_event_get_occurrences(self):
        event = Event.objects.get(pk=1)
        occurrences = event.get_occurrences(
            datetime(2014,8,1,0,0,0, tzinfo=utc), 
            datetime(2014,8,31,0,0,0, tzinfo=utc)
        )
        startdatetimes = [event.startdatetime for event in occurrences]
        self.assertTrue(len(occurrences) == 5)
        self.assertTrue(datetime(2014,8,9,0,10,0, tzinfo=utc) in startdatetimes)

    def test_get_recurrence_rule(self):
        event = Event.objects.get(pk=1)
        event_rule = event.get_recurrence_rule()
        rule = rrule(WEEKLY,byweekday=[SA,], until=datetime(2014,10,1,1,10,0, tzinfo=utc))
        self.assertEqual(rule._freq, event_rule._freq)
        self.assertEqual(rule._byweekday, event_rule._byweekday)
        self.assertEqual(rule._until, event_rule._until)
