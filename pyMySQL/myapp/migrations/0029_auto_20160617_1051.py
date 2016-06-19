# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_auto_20160616_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='CreatedOn',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Created On'),
        ),
    ]
