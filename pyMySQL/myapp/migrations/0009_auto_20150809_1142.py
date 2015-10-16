# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20150809_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='BankInstruction',
            field=models.URLField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='Comments',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='EndDate',
            field=models.DateField(default=datetime.datetime(2015, 8, 9, 18, 42, 56, 208000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='StartDate',
            field=models.DateField(default=datetime.datetime(2015, 8, 9, 18, 42, 56, 208000, tzinfo=utc)),
        ),
    ]
