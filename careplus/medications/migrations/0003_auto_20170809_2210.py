# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-10 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0002_medicationtime_timecreated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationtime',
            name='timeCreated',
            field=models.DateTimeField(verbose_name='Created'),
        ),
    ]