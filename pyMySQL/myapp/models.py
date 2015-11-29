from django.db import models
from django.contrib.auth.models import   User
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.template.defaultfilters import default
from django.conf import settings

# Create your models here.

class Vendor(models.Model):
    VendorId = models.AutoField(primary_key=True)
    VendorName = models.CharField(max_length=128, unique=True)
    Comments = models.CharField(max_length=1024, null=True)
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.VendorName)

class Company(models.Model):
    CompanyId = models.AutoField(primary_key=True)
    CompanyName = models.CharField(max_length=128, unique=True)
    BankInstruction = models.URLField(max_length=1024, null=True)
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.CompanyName)

class Status(models.Model):
    Status = models.CharField(max_length=32, primary_key=True)
    Description = models.CharField(max_length=1024)
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s, %s' % (self.Status, self.Description)
    
class PROJECT(models.Model):
    ProjectId = models.AutoField(primary_key=True)
    ProjectName = models.CharField(max_length=128, unique=True)
    DESCRIPTION = models.CharField(max_length=1024, unique=False)
    SinglePhase = models.BooleanField(default=True)
    Allocation = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    Committed = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    CompanyId = models.ForeignKey(Company, default="1")
    VendorId =  models.ForeignKey(Vendor, default="1")
    StartDate = models.DateField('Started On', default=datetime.now)
    EndDate = models.DateField('Ended On', default=datetime.now)
    Status =  models.ForeignKey(Status, default="open")
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.DESCRIPTION)

class TransactionType(models.Model):
    Type = models.CharField(primary_key=True, max_length=20, default="Deposit")
    Description = models.CharField(max_length=256, unique=False)
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s %s' % (self.Type, self.Description)
    
class InvestmentActivity(models.Model):
    ActivityId = models.AutoField(primary_key=True)
    UserId =models.ForeignKey(User, default="1")
    Type = models.ForeignKey(TransactionType, default="Deposit")
    Date = models.DateField(auto_now=False, auto_now_add=False,  null=True)
    ProjectId = models.ForeignKey(PROJECT, default="999")
    Memo = models.CharField(max_length=1024, unique=False)
    Amount = models.FloatField(default=0.0)
    CreatedOn = models.DateField('Creaetd On', default=datetime.now)

    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.UserId)

class InvestmentActivityCopy(models.Model):
    ActivityId = models.AutoField(primary_key=True)
    UserId =models.ForeignKey(User, default="1")
    Type = models.ForeignKey(TransactionType, default="Deposit")
    Date = models.DateField(auto_now=False, auto_now_add=False,  null=True)
    ProjectId = models.ForeignKey(PROJECT, default="999")
    Memo = models.CharField(max_length=1024, unique=False)
    Amount = models.FloatField(default=0.0)
    CreatedOn = models.DateField('Creaetd On', default=datetime.now)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return u'%s' % (self.UserId)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    #user = models.OneToOneField(User)
    #UserId =models.ForeignKey(User, primary_key=True)
    UserId =models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

    # The additional attributes we wish to include.
    Telephone = models.CharField('Phone#', max_length=32, null=True)
    Cell = models.CharField('Cell#', max_length=32, null=True)
    Address1 = models.CharField(max_length=256, null=True)
    Address2 = models.CharField(max_length=256, null=True)
    City = models.CharField(max_length=64, null=True)
    State = models.CharField(max_length=32, default="CA", null=True)
    ZipCode = models.CharField(max_length=16, null=True)
    W9Ready = models.BooleanField('W-9 Filed?', default=False)
    website = models.URLField(null=True)

    minCommitment = models.IntegerField(default=0)
    maxCommitment = models.IntegerField(default=0)
    lastCommitmentDate = models.DateField('Date Committed', default=datetime.now)
    
    #Bank instructions x 3
    bank1Name = models.CharField('Bank1 Name', max_length=64, null=True)
    bank1UserName = models.CharField('Bank1 Account Name', max_length=64, null=True)
    bank1Rounting = models.CharField('Bank1 ABA#', max_length=32, null=True)
    bank1AccountNumber = models.CharField('Bank1 Account#', max_length=32, null=True)
    
    bank2Name = models.CharField('Bank2 Name', max_length=64, null=True)
    bank2UserName = models.CharField('Bank2 Account Name', max_length=64, null=True)
    bank2Rounting = models.CharField('Bank2 ABA#', max_length=32, null=True)
    bank2AccountNumber = models.CharField('Bank2 Account#', max_length=32, null=True)

    bank3Name = models.CharField('Bank3 Name', max_length=64, null=True)
    bank3UserName = models.CharField('Bank3 Account Name', max_length=64, null=True)
    bank3Rounting = models.CharField('Bank3 ABA#', max_length=32, null=True)
    bank3AccountNumber = models.CharField('Bank3 Account#', max_length=32, null=True)
    
    #picture = models.ImageField(upload_to='profile_images')

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return u'%s' % (self.UserId)