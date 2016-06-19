# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_remove_userprofile_wechatid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wechatId',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
