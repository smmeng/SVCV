# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_userprofile_wechatid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='wechatId',
        ),
    ]
