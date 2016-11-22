from django.db import models
from django.contrib.auth.models import   User
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.template.defaultfilters import default
from django.conf import settings

# Create your models here.
class positionJSONHistory(models.Model):
    id = models.AutoField(primary_key=True )
    ICAO = models.CharField(max_length=8, null=True)
    Flight = models.CharField(max_length=10, null=True)
    date = models.DateTimeField('Created On', default=datetime.now, null=True)
    altitude = models.IntegerField(default=0, null=True)
    latitude = models.FloatField(default=0, null=True)
    longititude = models.FloatField(max_length=8, null=True)
    squawk = models.CharField(max_length=10, null=True)
    nucp = models.IntegerField(default=0, null=True)
    seen_pos = models.FloatField(max_length=8, null=True)
    vert_rate = models.IntegerField(default=0, null=True)
    track = models.IntegerField(default=0, null=True)
    speed = models.IntegerField(default=0, null=True)
    category = models.CharField(max_length=6, null=True)
    messages = models.IntegerField(default=0, null=True)
    seen = models.FloatField(max_length=8, null=True)
    rssi = models.FloatField(max_length=8, null=True)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.ICAO + "-" + self.Flight)


class Announcement(models.Model):
    AnnouncementId = models.AutoField(primary_key=True)
    OutputText = models.TextField(max_length=8192, null=False)
    Comments = models.CharField(max_length=1024, null=True)
    CreatedOn = models.DateTimeField('Created On', default=datetime.now)
    ExpireOn = models.DateField('Expire On', default=datetime.now)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % ( self.OutputText)
    
class flights(models.Model):
    id = models.AutoField(primary_key=True )
    ICAO = models.CharField(max_length=8, null=True)
    Flight = models.CharField(max_length=10, null=True)
    date = models.DateTimeField('Created On', default=datetime.now, null=True)
    altitude = models.IntegerField(default=0, null=True)
    latitude = models.FloatField(default=0, null=True)
    longitude = models.FloatField(max_length=8, null=True)
    aircraft = models.CharField(max_length=6, null=True)
    orig = models.CharField(max_length=6, null=True)
    dest = models.CharField(max_length=6, null=True)
    speed = models.IntegerField(default=0, null=True)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % ( self.ICAO + "-" + self.Flight)