from django.shortcuts import render
from django.db.models import Max, Min

# Create your views here.
from django.http import HttpResponse

from django.utils import timezone
from .models import SensorReading

SOURCE_PARAM = 'sourceName'
TEMPERATURE_PARAM = 'temperature'
HUMIDITY_PARAM = 'humidity'
LCI1_PARAM = 'lci1'
LCI2_PARAM = 'lci2'

def index(request):
    return HttpResponse('First version of the index page')

def reading_collector(request):
    mandatory_parameter = "You need to provide '%s' in your request.\n"
    if SOURCE_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % SOURCE_PARAM)
    if TEMPERATURE_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % TEMPERATURE_PARAM)
    if HUMIDITY_PARAM not in request.GET:
        return HttpResponse(mandatory_parameter % HUMIDITY_PARAM)

    sensor_reading = create_reading(request)
    sensor_reading.save()
    return HttpResponse('Received sensor reading from %s\n' % sensor_reading)

def create_reading(request):
    reading = SensorReading()
    reading.source = request.GET[SOURCE_PARAM]
    reading.reading_date = timezone.now()
    reading.temperature = request.GET[TEMPERATURE_PARAM]
    reading.humidity = request.GET[HUMIDITY_PARAM]
    if LCI1_PARAM in request.GET:
        reading.lci1_active = get_boolean_from_string(request.GET[LCI1_PARAM])

    if LCI2_PARAM in request.GET:
        reading.lci2_active = get_boolean_from_string(request.GET[LCI2_PARAM])

    return reading 

def get_boolean_from_string(string_value):
    return string_value.lower() in ("yes", "true", "t", "1")

def reading_post_collector(request):
    #source = request.POST.get('sourceName','unknownSource')
    #temperature = request.POST.get('temperatureReading', 0)
    #humidity = request.POST.get('humidityReading', 0)
    #sensor_reading = SensorReading(source=source,reading_date=timezone.now(),temperature=temperature,humidity=humidity)
    #sensor_reading.save()
    return HttpResponse('Received sensor reading through POST')
            
def report(request):
    latest_reading_date = SensorReading.objects.all().aggregate(Max('reading_date'))
    max_temperature = SensorReading.objects.all().aggregate(Max('temperature'))
    min_temperature = SensorReading.objects.all().aggregate(Min('temperature'))
    context = {'latest_reading_date': latest_reading_date['reading_date__max'],
               'max_temperature': max_temperature['temperature__max'],
               'min_temperature': min_temperature['temperature__min'],}
    return render(request, 'report.html', context)

