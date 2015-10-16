# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20150801_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='SinglePhase',
            field=models.BooleanField(default=True),
        ),
    ]
