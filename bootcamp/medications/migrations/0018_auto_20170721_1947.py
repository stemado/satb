# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-22 00:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0017_auto_20170720_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationtime',
            name='timeDue',
            field=models.TimeField(blank=True, null=True, verbose_name='Time Due'),
        ),
    ]