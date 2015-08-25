# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dracocollector', '0002_auto_20150802_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorreading',
            name='lci1_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sensorreading',
            name='lci2_active',
            field=models.BooleanField(default=False),
        ),
    ]
