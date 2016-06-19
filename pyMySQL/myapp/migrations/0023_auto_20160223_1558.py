# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0022_auto_20150818_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('AnnouncementId', models.AutoField(serialize=False, primary_key=True)),
                ('OutputText', models.CharField(max_length=8192)),
                ('Comments', models.CharField(max_length=1024, null=True)),
                ('CreatedOn', models.DateField(default=datetime.datetime.now, verbose_name=b'Creaetd On')),
                ('ExpireOn', models.DateField(verbose_name=b'Expire On')),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='project',
            name='website',
            field=models.URLField(default=b'', max_length=1024),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='UserId',
            field=models.OneToOneField(primary_key=True, default=999999, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank1AccountNumber',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank1 Account#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank1Name',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank1 Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank1Rounting',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank1 ABA#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank1UserName',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank1 Account Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank2AccountNumber',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank2 Account#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank2Name',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank2 Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank2Rounting',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank2 ABA#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank2UserName',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank2 Account Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank3AccountNumber',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank3 Account#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank3Name',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank3 Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank3Rounting',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Bank3 ABA#'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bank3UserName',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Bank3 Account Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastCommitmentDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Date Committed'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='maxCommitment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='minCommitment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investmentactivity',
            name='CreatedOn',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Creaetd On'),
        ),
        migrations.AlterField(
            model_name='investmentactivity',
            name='ProjectId',
            field=models.ForeignKey(related_name='InvestmentActivity', default=b'999', to='myapp.PROJECT'),
        ),
        migrations.AlterField(
            model_name='investmentactivity',
            name='Type',
            field=models.ForeignKey(related_name='InvestmentActivity', default=b'Deposit', to='myapp.TransactionType'),
        ),
        migrations.AlterField(
            model_name='investmentactivity',
            name='UserId',
            field=models.ForeignKey(related_name='InvestmentActivity', default=b'1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investmentactivitycopy',
            name='CreatedOn',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Creaetd On'),
        ),
        migrations.AlterField(
            model_name='project',
            name='EndDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Ended On'),
        ),
        migrations.AlterField(
            model_name='project',
            name='StartDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Started On'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Cell',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Cell#'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Telephone',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Phone#'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='W9Ready',
            field=models.BooleanField(default=False, verbose_name=b'W-9 Filed?'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(null=True),
        ),
    ]
