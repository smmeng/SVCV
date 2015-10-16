# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0015_investactivity_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentActivity',
            fields=[
                ('ActivityId', models.AutoField(serialize=False, primary_key=True)),
                ('Type', models.CharField(default=b'Deposit', max_length=20)),
                ('Date', models.DateField(null=True)),
                ('Memo', models.CharField(max_length=1024)),
                ('Amount', models.DecimalField(default=Decimal('0.00'), max_digits=20, decimal_places=2)),
                ('ProjectId', models.ForeignKey(default=b'999', to='myapp.PROJECT')),
                ('UserId', models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='investactivity',
            name='ProjectId',
        ),
        migrations.RemoveField(
            model_name='investactivity',
            name='UserId',
        ),
        migrations.DeleteModel(
            name='InvestActivity',
        ),
    ]
