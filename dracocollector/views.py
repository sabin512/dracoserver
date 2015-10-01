import json
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

def index(request):
    return HttpResponse('First version of the index page')

@csrf_exempt
def reading_post_collector(request):
    mandatory_parameter = "You need to provide '%s' in your request.\n"
    webhookJsonData = json.loads(request.body.decode('utf-8'))
    #this is bullshit because html.unescape doesn't exist in python 3.2
    unescapedData = webhookJsonData['data'].replace('&quot;','"')
    jsonData = json.loads(unescapedData)

    if SOURCE_PARAM not in jsonData:
        return HttpResponse(mandatory_parameter % SOURCE_PARAM)
    if TEMPERATURE_PARAM not in jsonData:
        return HttpResponse(mandatory_parameter % TEMPERATURE_PARAM)
    if HUMIDITY_PARAM not in jsonData:
        return HttpResponse(mandatory_parameter % HUMIDITY_PARAM)

    sensor_reading = create_reading(jsonData)
    sensor_reading.save()
    return HttpResponse('Received sensor reading through POST')

def reading_collector(request):
    mandatory_parameter = "You need to provide '%s' in your request.\n"
    if SOURCE_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % SOURCE_PARAM)
    if TEMPERATURE_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % TEMPERATURE_PARAM)
    if HUMIDITY_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % HUMIDITY_PARAM)

    sensor_reading = create_reading(request.GET)
    sensor_reading.save()
    return HttpResponse('Received sensor reading from %s\n' % sensor_reading)

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
        form = ExportPrepareForm()

    return render(request, 'prepareExport.html', {'form': form})

class SensorReadingCSVWriter(object):
    def write(self, value):
        return value 

def export_data(form):
    source_to_export = form.cleaned_data['source_name']
    all_readings = SensorReading.objects.filter(source=source_to_export)
    pseudo_buffer = SensorReadingCSVWriter()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(get_reading_data_as_list(reading)) for reading in all_readings),
                                     content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="readingData.csv"'
    return response

def get_reading_data_as_list(reading):
    return [reading.source, reading.reading_date, reading.temperature, reading.humidity, reading.lci1_active, reading.lci2_active]
