from django.db import models
from djangotoolbox.fields import ListField
#from mongoengine import *
#from mongoengine.base import metaclasses
# Create your models here.
#class vistorType(models.Model):
from datetime import datetime

from django import forms
from bson.json_util import default

class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]
    
class MyListField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)


class vistorType(models.Model):
    Type = models.CharField(primary_key=True, max_length=100, unique=True) #pnote or equity
    Description = models.CharField(max_length=1024)
    Comments = MyListField()
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.Type)

class employee(models.Model):
    employeeId = models.IntegerField(primary_key=True, default=999999)
    employeeName = models.CharField(max_length=128)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.employeeName)
        
    
class visitorLog(models.Model):
    #visitorLogId= models.IntegerField(unique=True, default=999999)
    #id= models.IntegerField(primary_key=True)
    Type = models.ForeignKey(vistorType, default="Visitor") #pnote or equity
    fname =models.CharField(max_length=128)
    lname =models.CharField(max_length=128)
    email=models.CharField(max_length=128)
    phone=models.CharField(max_length=128)
    employeeId=models.ForeignKey(employee)
    Comments = models.CharField(max_length=1024)
    CreatedOn = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.fname+' '+self.lname)
'''
class vistorType(Document):
    Type = StringField(required=True, max_length=100)
    Description = StringField(max_length=1024)
    objects = models.Manager()
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.Description)
'''
