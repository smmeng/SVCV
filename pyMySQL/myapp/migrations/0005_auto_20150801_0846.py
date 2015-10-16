# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20150801_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='CompanyId',
            field=models.CharField(default=b'0', max_length=4),
        ),
        migrations.AddField(
            model_name='project',
            name='VendorId',
            field=models.CharField(default=b'0', max_length=4),
        ),
    ]
