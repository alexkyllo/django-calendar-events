from django import forms
from models import *
from widgets import *
from dateutil import rrule
from django.forms.extras.widgets import SelectDateWidget

DAY_CHOICES = (
    (0,"Monday"),
    (1,"Tuesday"),
    (2,"Wednesday"),
    (3,"Thursday"),
    (4,"Friday" ),
    (5,"Saturday"),
    (6,"Sunday"),
)

# Widget
class CSICheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        # Return a string of comma separated integers since the database, and
        # field expect a string (not a list).
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        # Convert comma separated integer string to a list, since the checkbox
        # rendering code expects a list (not a string)
        if value:
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )


# Form field
class CSIMultipleChoiceField(forms.MultipleChoiceField):
    widget = CSICheckboxSelectMultiple

    # Value is stored and retrieved as a string of comma separated
    # integers. We don't want to do processing to convert the value to
    # a list like the normal MultipleChoiceField does.
    def to_python(self, value):
        return value

    def validate(self, value):
        # If we have a value, then we know it is a string of comma separated
        # integers. To use the MultipleChoiceField validator, we first have
        # to convert the value to a list.
        if value:
            value = value.split(',')
        super(CSIMultipleChoiceField, self).validate(value)

class EventForm(forms.ModelForm):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", required=True, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", required=False, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    recurring = forms.BooleanField(required=False, initial=False)
    byweekday = CSIMultipleChoiceField(label="Recur on weekdays", required=False, choices=DAY_CHOICES, widget=CSICheckboxSelectMultiple)
    until = forms.DateField(label="Recur until", required=False, widget=SelectDateWidget())

    class Meta:
        model = Event




