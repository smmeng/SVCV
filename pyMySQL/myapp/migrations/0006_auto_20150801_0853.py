# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20150801_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ProjectId',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
