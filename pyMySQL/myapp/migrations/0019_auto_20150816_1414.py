# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20150815_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentactivity',
            name='Amount',
            field=models.FloatField(default=0.0),
        ),
    ]
