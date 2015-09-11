from django import forms
from .models import SensorReading

def get_source_choices():
    source_names = SensorReading.objects.order_by().values_list('source',flat=True).distinct()
    return [(source,source) for source in source_names]

class ExportPrepareForm(forms.Form):
    source_name = forms.ChoiceField(label='Source to export', choices=get_source_choices())

