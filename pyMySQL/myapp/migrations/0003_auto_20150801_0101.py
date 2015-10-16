# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20150629_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='PROJECT',
            fields=[
                ('ProjectId', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('ProjectName', models.CharField(unique=True, max_length=128)),
                ('DESCRIPTION', models.CharField(max_length=102428)),
                ('SinglePhase', models.BooleanField()),
                ('Allocation', models.DecimalField(default=Decimal('0.00'), max_digits=20, decimal_places=2)),
                ('Committed', models.DecimalField(default=Decimal('0.00'), max_digits=20, decimal_places=2)),
            ],
        ),
        migrations.DeleteModel(
            name='Groups',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='Users_Groups',
        ),
    ]
