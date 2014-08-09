django-calendar-events
======================

A Django app plugin for recurring calendar events.

Ever needed to put a calendar in your Django site? This app provides an easy way to do that. It is designed to work with the Arshaw jquery-ui fullcalendar widget.

It includes:
+ An Event model for saving a calendar event to the database
+ Event model methods for returning JSON-serialized events for the fullcalendar API
+ Event model fields for storing event recurrence rules based on the dateutil.rrule api
+ A template for displaying the fullcalendar widget
+ Django forms for creating and updating calendar events