from django.db import models
from mongoengine import Document, StringField
# Create your models here.
#class vistorType(models.Model):


class vistorType(models.Model):
    Type = models.CharField(primary_key=True, max_length=100) #pnote or equity
    Description = models.CharField(max_length=1024)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.Description)
'''

class vistorType(Document):
    Type = StringField(required=True, max_length=100)
    Description = StringField(max_length=1024)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.Description)
    
'''