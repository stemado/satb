# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-08 05:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0003_auto_20170707_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='medicationRecordReset',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
