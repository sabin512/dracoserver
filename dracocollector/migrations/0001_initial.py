# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=100)),
                ('reading_date', models.DateTimeField(verbose_name='date of reading')),
                ('temperature', models.FloatField(default=0.0)),
                ('humidity', models.IntegerField(default=0)),
            ],
        ),
    ]
