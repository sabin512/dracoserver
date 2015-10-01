import json
from datetime import date
from django.shortcuts import render
from django.db.models import Max, Min
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect

from django.utils import timezone
from .models import SensorReading
from .forms import ExportPrepareForm

import csv

SOURCE_PARAM = 'sourceName'
TEMPERATURE_PARAM = 'temperature'
HUMIDITY_PARAM = 'humidity'
LCI1_PARAM = 'lci1'
LCI2_PARAM = 'lci2'

MANDATORY_FIELDS = [SOURCE_PARAM, TEMPERATURE_PARAM, HUMIDITY_PARAM]

def index(request):
    return HttpResponse('First version of the index page')

@csrf_exempt
def reading_post_collector(request):
    webhookJsonData = json.loads(request.body.decode('utf-8'))
    if 'data' not in webhookJsonData:
        return HttpResponse("JSON data needs to be in JSON field 'data'\n")
    #this is bullshit because html.unescape doesn't exist in python 3.2
    unescapedData = webhookJsonData['data'].replace('&quot;','"')
    jsonData = json.loads(unescapedData)

    missing_fields = find_missing_fields(jsonData)
    if missing_fields:
        return create_missing_fields_response(missing_fields)

    sensor_reading = create_reading(jsonData)
    sensor_reading.save()
    return HttpResponse('Received sensor reading through POST')

def reading_collector(request):
    missing_fields = find_missing_fields(request.GET)
    if missing_fields:
        return create_missing_fields_response(missing_fields)

    sensor_reading = create_reading(request.GET)
    sensor_reading.save()
    return HttpResponse('Received sensor reading from %s\n' % sensor_reading)

def create_missing_fields_response(missing_fields):
    return HttpResponse('You need to provide the fields: %s\n' % missing_fields)

def find_missing_fields(data):
    return [p for p in MANDATORY_FIELDS if p not in data]

def create_reading(request_params):
    reading = SensorReading()
    reading.source = request_params[SOURCE_PARAM]
    reading.reading_date = timezone.now()
    reading.temperature = request_params[TEMPERATURE_PARAM]
    reading.humidity = request_params[HUMIDITY_PARAM]
    if LCI1_PARAM in request_params:
        reading.lci1_active = get_boolean_from_string(request_params[LCI1_PARAM])

    if LCI2_PARAM in request_params:
        reading.lci2_active = get_boolean_from_string(request_params[LCI2_PARAM])

    return reading 

def get_boolean_from_string(string_value):
    return string_value.lower() in ("yes", "true", "t", "1")

def report(request):
    latest_reading_date = SensorReading.objects.all().aggregate(Max('reading_date'))
    max_temperature = SensorReading.objects.all().aggregate(Max('temperature'))
    min_temperature = SensorReading.objects.all().aggregate(Min('temperature'))
    context = {'latest_reading_date': latest_reading_date['reading_date__max'],
               'max_temperature': max_temperature['temperature__max'],
               'min_temperature': min_temperature['temperature__min'],}
    return render(request, 'report.html', context)


def export_csv(request):
    if request.method == 'POST':
        form = ExportPrepareForm(request.POST)
        if form.is_valid():
            return export_data(form)
    else:
        default_start_date = date.today()
        form = ExportPrepareForm(initial={'start_date': default_start_date})

    return render(request, 'prepareExport.html', {'form': form})

class SensorReadingCSVWriter(object):
    def write(self, value):
        return value 

def export_data(form):
    source_to_export = form.cleaned_data['source_name']
    start_date_to_export = form.cleaned_data['start_date']
    all_readings = SensorReading.objects.filter(source=source_to_export,reading_date__gte=start_date_to_export)
    pseudo_buffer = SensorReadingCSVWriter()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(get_reading_data_as_list(reading)) for reading in all_readings),
                                     content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="readingData.csv"'
    return response

def get_reading_data_as_list(reading):
    return [reading.source, reading.reading_date, reading.temperature, reading.humidity, reading.lci1_active, reading.lci2_active]
