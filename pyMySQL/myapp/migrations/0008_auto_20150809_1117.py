# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_company_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('Status', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('Description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='EndDate',
            field=models.DateField(default=datetime.datetime(2015, 8, 9, 18, 17, 0, 565000, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='project',
            name='StartDate',
            field=models.DateField(default=datetime.datetime(2015, 8, 9, 18, 17, 0, 565000, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='project',
            name='Status',
            field=models.CharField(default=b'open', max_length=32),
        ),
        migrations.AlterField(
            model_name='project',
            name='DESCRIPTION',
            field=models.CharField(max_length=1024),
        ),
    ]
