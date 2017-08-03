# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-03 03:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='residentGender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=30, null=True, verbose_name='Gender'),
        ),
    ]
