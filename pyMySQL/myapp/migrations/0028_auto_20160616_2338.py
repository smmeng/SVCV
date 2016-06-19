# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_auto_20160412_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='OutputText',
            field=models.TextField(max_length=8192),
        ),
    ]
