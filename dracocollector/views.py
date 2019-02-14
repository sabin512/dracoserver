import json
import requests
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Max, Min
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect

from django.utils import timezone
from .models import SensorReading
from .models import TelemetryProbe
from .forms import ExportPrepareForm

import csv

SOURCE_PARAM = 'sourceName'
FW_VERSION = 'fwVersion'
TEMPERATURE_PARAM = 'temperature'
HUMIDITY_PARAM = 'humidity'
LCI1_PARAM = 'lci1'
LCI2_PARAM = 'lci2'
PULL_DATA_URL = 'https://api.particle.io/v1/devices/%s/%s?access_token=%s'
PULL_REQUEST_HEADERS={'content-type': 'application/x-www-form-urlencoded'}

MANDATORY_FIELDS = [SOURCE_PARAM, FW_VERSION, TEMPERATURE_PARAM, HUMIDITY_PARAM]

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
    reading.fw_version = request_params[FW_VERSION]
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
    if SOURCE_PARAM not in request.GET:
        return HttpResponse('You need to specify a telemetry probe name using parameter %s' % SOURCE_PARAM)

    source_name = request.GET[SOURCE_PARAM]
    try:
        probe = TelemetryProbe.objects.get(name=source_name)
    except ObjectDoesNotExist:
        return HttpResponse('Telemetry probe %s is not registered, no data will be reported' % source_name)

    all_data = SensorReading.objects.filter(source=source_name).aggregate(Max('temperature'),
                                                                          Min('temperature'),
                                                                          Max('reading_date'),
                                                                          Max('humidity'),
                                                                          Min('humidity'))

    recent_start = date.today() - timedelta(days=2)
    recent_end = date.today()

    recent_data = SensorReading.objects.filter(source=source_name,
                                               reading_date__range=[recent_start, recent_end]).aggregate(Max('temperature'),
                                                                                                         Min('temperature'),
                                                                                                         Max('humidity'),
                                                                                                         Min('humidity'))

    uptime = retrieve_uptime(probe)
    temperature = pull_probe_data(probe, 'temp')
    humidity = pull_probe_data(probe, 'humidity')
    counter = pull_probe_data(probe, 'rCounter')
    lci1reading = pull_probe_data(probe, 'lci1')
    lci2reading = pull_probe_data(probe, 'lci2')

    context = {'latest_reading_date': all_data['reading_date__max'],
               'uptime_data': uptime,
               'source_name': source_name,
               'restart_counter': counter,
               'lci1_reading': lci1reading,
               'lci2_reading': lci2reading,
               'curr_temperature': temperature,
               'curr_humidity': humidity,
               'max_temperature': all_data['temperature__max'],
               'min_temperature': all_data['temperature__min'],
               'max_humidity': all_data['humidity__max'],
               'min_humidity': all_data['humidity__min'],
               'recent_max_temperature': recent_data['temperature__max'],
               'recent_min_temperature': recent_data['temperature__min'],
               'recent_max_humidity': recent_data['humidity__max'],
               'recent_min_humidity': recent_data['humidity__min']}
    return render(request, 'report.html', context)

def pull_probe_data(probe, field_name):
    complete_pull_url = PULL_DATA_URL % (probe.device_id, field_name, probe.access_token)
    response = requests.get(complete_pull_url, PULL_REQUEST_HEADERS)
    if response.status_code != 200:
       return 'Failed to retrieve %s' % field_name
    return response.json()['result']

@csrf_exempt
def get_uptime(request):
    if SOURCE_PARAM not in request.GET:
        return HttpResponse('No probe name specified using %s parameter.' % SOURCE_PARAM)
    source_name = request.GET[SOURCE_PARAM]
    try:
        probe = TelemetryProbe.objects.get(name=source_name)
    except ObjectDoesNotExist:
        return HttpResponse('Telemetry probe %s is not registered, no data will be reported' % source_name)
    return HttpResponse(retrieve_uptime(probe))

def retrieve_uptime(probe):
    start_date = datetime.fromtimestamp(pull_probe_data(probe, 'startTime'))
    time_lapsed = str(datetime.now() - start_date).split('.')[0]
    return str(time_lapsed)

#Work in progress for the get_live_data view
def get_live_data(request):
    if SOURCE_PARAM not in request.GET:
        return HttpResponse('No probe name specified using %s parameter.' % SOURCE_PARAM)
    source_name = request.GET[SOURCE_PARAM]
    try:
        probe = TelemetryProbe.objects.get(name=source_name)
    except ObjectDoesNotExist:
        return HttpResponse('Telemetry probe %s is not registered, no data will be reported' % source_name)

    probe_data = {}
    probe_data['uptime'] = retrieve_uptime(probe)
    probe_data['temperature'] = '%.1f' % pull_probe_data(probe, 'temp')
    probe_data['humidity'] = '%.1f' % pull_probe_data(probe, 'humidity')
    probe_data['counter'] = pull_probe_data(probe, 'rCounter')
    probe_data['lci1'] = pull_probe_data(probe, 'lci1')
    probe_data['lci2'] = pull_probe_data(probe, 'lci2')
    probe_data['readingCount'] = SensorReading.objects.filter(source=source_name).count()
    return HttpResponse(json.dumps(probe_data))

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
