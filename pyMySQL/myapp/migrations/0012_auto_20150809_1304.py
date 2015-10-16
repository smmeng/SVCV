# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20150809_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='CompanyId',
            field=models.ForeignKey(default=b'1', to='myapp.Company'),
        ),
        migrations.AlterField(
            model_name='project',
            name='VendorId',
            field=models.ForeignKey(default=b'1', to='myapp.Vendor'),
        ),
    ]
