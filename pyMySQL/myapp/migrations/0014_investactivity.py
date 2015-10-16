# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestActivity',
            fields=[
                ('ActivityId', models.AutoField(serialize=False, primary_key=True)),
                ('Type', models.CharField(default=b'Deposit', max_length=20)),
                ('Date', models.DateField(null=True)),
                ('Memo', models.CharField(max_length=1024)),
                ('Amount', models.DecimalField(default=Decimal('0.00'), max_digits=20, decimal_places=2)),
                ('ProjectId', models.ForeignKey(default=b'999', to='myapp.PROJECT')),
            ],
        ),
    ]
