# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-11 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0002_auto_20170711_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='medicationStatus2',
            field=models.CharField(choices=[('False', 'Not Given'), ('True', 'Given')], default=False, max_length=10, verbose_name='Current Status 2'),
        ),
    ]
