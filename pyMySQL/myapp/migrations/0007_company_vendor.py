# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20150801_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('CompanyId', models.AutoField(serialize=False, primary_key=True)),
                ('CompanyName', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('VendorId', models.AutoField(serialize=False, primary_key=True)),
                ('VendorName', models.CharField(unique=True, max_length=128)),
            ],
        ),
    ]
