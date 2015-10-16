# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_auto_20150818_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='Address1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Address2',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Cell',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='City',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='State',
            field=models.CharField(default=b'CA', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Telephone',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='W9Ready',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ZipCode',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
