from django.contrib import admin

# Register your models here.
from .models import SensorReading

class SensorReadingAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Snapshot Information', {'fields':['reading_date','source']}),
            ('Reading Data',         {'fields':['temperature','humidity','lci1_active','lci2_active']}),
    ]

    list_filter = ['reading_date','lci1_active', 'lci2_active']
    list_display = ['source', 'reading_date', 'temperature', 'humidity', 'lci1_active', 'lci2_active']
    search_fields = ['source']

admin.site.register(SensorReading, SensorReadingAdmin)
