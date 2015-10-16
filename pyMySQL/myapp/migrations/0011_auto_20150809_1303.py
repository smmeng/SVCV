# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20150809_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='CompanyId',
            field=models.ForeignKey(to='myapp.Company'),
        ),
        migrations.AlterField(
            model_name='project',
            name='Status',
            field=models.ForeignKey(default=b'open', to='myapp.Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='VendorId',
            field=models.ForeignKey(to='myapp.Vendor'),
        ),
    ]
