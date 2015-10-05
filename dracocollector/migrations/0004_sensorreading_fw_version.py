# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dracocollector', '0003_auto_20150824_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorreading',
            name='fw_version',
            field=models.CharField(default='1.0', max_length=100),
        ),
    ]
