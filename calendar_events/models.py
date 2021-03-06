from django.db import models
from django.contrib.auth.models import User
from dateutil.rrule import *
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.forms.util import from_current_timezone

# Create your models here.

FREQUENCY_CHOICES = (
    ('YEARLY','yearly'),
    ('MONTHLY','monthly'),
    ('WEEKLY','weekly'),
    ('DAILY','daily'),
)

WEEKDAYS = ('MO','TU','WE','TH','FR','SA','SU')
WEEKDAY_NAMES = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

DAY_CHOICES = (
    (0,"Monday"),
    (1,"Tuesday"),
    (2,"Wednesday"),
    (3,"Thursday"),
    (4,"Friday" ),
    (5,"Saturday"),
    (6,"Sunday"),
)

class Event(models.Model):
    '''
    This class defines a calendar event instance, which may be one-time or recurring (using dateutil.rrule)
    '''
    name = models.CharField(max_length=36)
    startdatetime = models.DateTimeField(blank=True, null=True)
    enddatetime = models.DateTimeField(blank=True, null=True)
    allday = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, blank=True)
    byweekday = models.CommaSeparatedIntegerField(max_length=36, blank=True)
    until = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.allday == True:
            self.startdatetime = from_current_timezone(datetime(self.startdatetime.year, self.startdatetime.month, self.startdatetime.day))
            self.enddatetime = from_current_timezone(datetime(self.startdatetime.year, self.startdatetime.month, self.startdatetime.day + 1))
        if self.until:
            self.until = from_current_timezone(self.until)
        #self.byweekday = [int(day) for day in self.byweekday]
        super(Event, self).save(*args, **kwargs)

    def get_rule_params(self):
        return {
                'byweekday':[eval(WEEKDAYS[int(day)]) if self.byweekday is not None else '' for day in self.byweekday.split(',')],
                'until':self.until,
            }

    def get_recurrence_rule(self):
        '''
        Returns the dateutil.rrule object instance associated with this Event
        '''
        if self.recurring:
            return rrule(eval(self.frequency), dtstart=self.startdatetime, **self.get_rule_params())
        return None

    def get_occurrences(self, start, end):
        '''
        Accepts start and end datetime objects and returns a list of Event objects that fall between the start and end date arguments,
        representing occurrences of this particular event. 
        '''
        if self.recurring:
            rule = self.get_recurrence_rule()
            recurrence_dates = rule.between(start, end, inc=True)
            duration = self.enddatetime - self.startdatetime
            events = [Event(
                id=self.id,
                name=self.name, 
                startdatetime=date,
                enddatetime=date+duration,
                allday=self.allday,
            ) for date in recurrence_dates]
            return events
        else:
            if (self.startdatetime >= start):
                return [self]
            else: 
                return []

    def get_month_occurrences(self, *args, **kwargs):
        '''
        Takes a year and month as arguments and returns a list of datetime objects representing the 
        occurrences of the event during the specified month
        '''
        year = kwargs['year']
        month = kwargs['month']
        if month not in range(1, 13):
            raise Exception("Month must be between 1 and 12.")
        occurrences = self.get_occurrences(start=datetime(year, month, 1, tzinfo=utc), end=datetime(year, month+1, 1, tzinfo=utc))
        return occurrences 

    def get_week_occurrences(self, *args, **kwargs):
        '''
        Takes a year, and week as arguments and returns a list of datetime objects representing the occurrences 
        of the event during the specified week
        '''
        year = kwargs['year']
        week = kwargs['week']
        start_of_week = datetime.strptime(str(year) + str(week) +"0+0000","%Y%U%w%z")
        if week not in range(1,54):
            raise Exception("Week must be between 1 and 53")
        occurrences = self.get_occurrences(start=start_of_week, end=start_of_week+timedelta(weeks=1))
        return occurrences

    def to_fullcalendar(self):
        event_dict = {}
        event_dict['id'] = self.id
        event_dict['title'] = self.name
        event_dict['allDay'] = self.allday
        event_dict['start'] = self.startdatetime.isoformat()
        event_dict['end'] = self.enddatetime.isoformat()
        event_dict['url'] = self.get_absolute_url()
        return event_dict

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('event_detail', args=[str(self.id)])

    def get_weekdays(self):
        return [WEEKDAY_NAMES[int(x)] for x in self.byweekday.split(',')]

    def __unicode__(self):
        return self.name