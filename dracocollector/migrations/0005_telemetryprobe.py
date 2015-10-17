# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dracocollector', '0004_sensorreading_fw_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelemetryProbe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('device_id', models.CharField(max_length=50)),
                ('access_token', models.CharField(max_length=50)),
            ],
        ),
    ]
