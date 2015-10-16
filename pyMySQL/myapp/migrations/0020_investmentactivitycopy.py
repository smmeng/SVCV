# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0019_auto_20150816_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentActivityCopy',
            fields=[
                ('ActivityId', models.AutoField(serialize=False, primary_key=True)),
                ('Date', models.DateField(null=True)),
                ('Memo', models.CharField(max_length=1024)),
                ('Amount', models.FloatField(default=0.0)),
                ('ProjectId', models.ForeignKey(default=b'999', to='myapp.PROJECT')),
                ('Type', models.ForeignKey(default=b'Deposit', to='myapp.TransactionType')),
                ('UserId', models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
