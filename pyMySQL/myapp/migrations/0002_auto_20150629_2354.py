# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groups',
            old_name='description',
            new_name='DESCRIPTION',
        ),
        migrations.RenameField(
            model_name='groups',
            old_name='groupId',
            new_name='GROUPID',
        ),
        migrations.RenameField(
            model_name='groups',
            old_name='groupName',
            new_name='GROUPNAME',
        ),
    ]
