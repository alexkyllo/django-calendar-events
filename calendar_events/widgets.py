from django import forms

class DateTimeWidget(forms.MultiWidget):
    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]