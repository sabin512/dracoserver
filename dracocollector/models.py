import datetime
from django.db import models

# Create your models here.
class SensorReading(models.Model):
    source = models.CharField(max_length=100)
    reading_date = models.DateTimeField('date of reading')
    temperature = models.FloatField(default=0.000000)
    humidity = models.FloatField(default=0.000000)
    lci1_active = models.BooleanField(default=False)
    lci2_active = models.BooleanField(default=False)
    fw_version = models.CharField(max_length=100,default='1.0')
    
    def __str__(self):
        return '%s on %s data[ver=%s, t=%s, h=%s, lci1=%s, lci2=%s]' % (self.source, 
                                                                        self.reading_date.strftime('%c'),
                                                                        self.fw_version,
                                                                        self.temperature, 
                                                                        self.humidity,
                                                                        self.lci1_active, 
                                                                        self.lci2_active)
