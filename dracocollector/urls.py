from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^sendReading$', views.reading_collector, name='collector'),
        url(r'^sendPostReading$', views.reading_post_collector, name='post_collector'),        
        url(r'^readingReport$', views.report, name='report'),
        url(r'^exportCSV$', views.export_csv, name='exportCSV'),
]
