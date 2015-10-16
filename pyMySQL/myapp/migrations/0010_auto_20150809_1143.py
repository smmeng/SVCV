# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20150809_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='EndDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='StartDate',
            field=models.DateField(null=True),
        ),
    ]
