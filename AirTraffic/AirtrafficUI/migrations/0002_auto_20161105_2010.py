# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-06 03:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AirtrafficUI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positionjsonhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name=b'Created On'),
        ),
    ]
