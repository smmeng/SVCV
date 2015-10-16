# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_investmentactivitycopy'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentactivity',
            name='CreatedOn',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='investmentactivitycopy',
            name='CreatedOn',
            field=models.DateField(null=True),
        ),
    ]
