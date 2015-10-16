# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20150815_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('Type', models.CharField(default=b'Deposit', max_length=20, serialize=False, primary_key=True)),
                ('Description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AlterField(
            model_name='investmentactivity',
            name='Type',
            field=models.ForeignKey(default=b'Deposit', to='myapp.TransactionType'),
        ),
    ]
