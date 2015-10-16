# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupId', models.CharField(unique=True, max_length=128)),
                ('groupName', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.CharField(unique=True, max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('salt', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Users_Groups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupId', models.CharField(max_length=128)),
                ('userId', models.CharField(max_length=128)),
            ],
        ),
    ]
