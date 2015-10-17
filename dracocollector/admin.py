from django.contrib import admin

# Register your models here.
from .models import SensorReading
from .models import TelemetryProbe

class SensorReadingAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Snapshot Information', {'fields':['reading_date','source','fw_version']}),
            ('Reading Data',         {'fields':['temperature','humidity','lci1_active','lci2_active']}),
    ]

    list_filter = ['reading_date','lci1_active', 'lci2_active']
    list_display = ['source', 'fw_version', 'reading_date', 'temperature', 'humidity', 'lci1_active', 'lci2_active']
    search_fields = ['source']

admin.site.register(SensorReading, SensorReadingAdmin)
admin.site.register(TelemetryProbe)
