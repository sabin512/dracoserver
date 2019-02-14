from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^index$', views.index, name='index'),
        url('sendReading$', views.reading_collector, name='collector'),
        url('sendPostReading$', views.reading_post_collector, name='post_collector'),
        url('/iotowl/dracocollector/readingReport$', views.report, name='report'),
        url('exportCSV$', views.export_csv, name='exportCSV'),
        url('getUptime$', views.get_uptime, name='getUptime'),
        url('getLiveData$', views.get_live_data, name='getLiveData'),
]
