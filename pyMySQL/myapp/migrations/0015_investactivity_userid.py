# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0014_investactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='investactivity',
            name='UserId',
            field=models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL),
        ),
    ]
