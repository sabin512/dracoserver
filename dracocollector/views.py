from django.shortcuts import render
from django.db.models import Max, Min

# Create your views here.
from django.http import HttpResponse

from django.utils import timezone
from .models import SensorReading

def index(request):
    return HttpResponse('First version of the index page')

def reading_collector(request):
    mandatory_parameter = 'You need to provide \'%s\' in your request.\n'
    if 'sourceName' not in request.GET:
        return HttpResponse(mandatory_parameter % 'sourceName')
    if 'temperatureReading' not in request.GET:
        return HttpResponse(mandatory_parameter % 'temperatureReading')
    if 'humidityReading' not in request.GET:
        return HttpResponse(mandatory_parameter % 'humidityReading')

    sensor_reading = create_reading(request)
    sensor_reading.save()
    return HttpResponse('Received sensor reading from %s\n' % sensor_reading)

def create_reading(request):
    source_name = request.GET['sourceName']
    temperature = request.GET['temperatureReading']
    humidity = request.GET['humidityReading']
    return SensorReading(source=source_name,reading_date=timezone.now(),temperature=temperature,humidity=humidity)

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

