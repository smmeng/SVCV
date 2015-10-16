# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_auto_20150815_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiontype',
            name='Description',
            field=models.CharField(max_length=256),
        ),
    ]
