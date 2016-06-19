# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_userprofile_wechatid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('ProjectType', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('Description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='BankInstruction',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Bank Instruction', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='CompanyName',
            field=models.CharField(unique=True, max_length=128, verbose_name=b'Company Name'),
        ),
    ]
