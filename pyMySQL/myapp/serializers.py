from rest_framework import serializers
from myapp.models import InvestmentActivity, PROJECT, TransactionType, UserProfile #Vendor, Company, Status,  
from django.contrib.auth.models import   User
from django.db.models import Sum,Q

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #InvestorList = serializers.HyperlinkedRelatedField(many=True, view_name='InvestorViewSet', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'full_name')

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

class InvestorSerializer(serializers.HyperlinkedModelSerializer):
    Type  = serializers.ReadOnlyField(source='Type.Description')
    ProjectId = serializers.ReadOnlyField(source='ProjectId.ProjectName')
    UserId = serializers.ReadOnlyField(source='UserId.username')
    first_name = serializers.ReadOnlyField(source='UserId.first_name')
    last_name = serializers.ReadOnlyField(source='UserId.last_name')
    #user_full_name = serializers.SerializerMethodField()
    
    class Meta:
        # Provide an association between the ModelForm and a model
        #UserFirstName = serializers.HyperlinkedIdentityField(source='User.first_name')
        #UserLastName = serializers.ReadOnlyField(source='User.last_name')
        
        model = InvestmentActivity
        fields = ('UserId', 'first_name', 'last_name', 'Type',  'ProjectId', 'Amount', 'Date')
        
        
class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = PROJECT
        fields = ('ProjectId', 'ProjectName', 'DESCRIPTION','Allocation', 'Committed', 'StartDate', 'EndDate', 'VendorId', 'CompanyId', 'Status', 'website', 'SinglePhase')
        
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    UserId = serializers.ReadOnlyField(source='UserId.username')
    first_name = serializers.ReadOnlyField(source='UserId.first_name')
    last_name = serializers.ReadOnlyField(source='UserId.last_name')
    email = serializers.ReadOnlyField(source='UserId.email')
    #isStaff = serializers.ReadOnlyField(source='UserId.is_staff')
    
    class Meta:
        # Provide an association between the ModelForm and a model
        
        model = UserProfile
        fields = ('UserId',  'first_name', 'last_name', 'email', 'Telephone', 'Cell', 'Address1', 'Address2', 'City', 'State', 'ZipCode', 'W9Ready', 'website', 
                  'minCommitment', 'maxCommitment', 'lastCommitmentDate')
        
class InvestorProfitSerializer(serializers.HyperlinkedModelSerializer):
    UserId = serializers.ReadOnlyField(source='UserId__username')
    first_name = serializers.ReadOnlyField(source='UserId__first_name')
    last_name = serializers.ReadOnlyField(source='UserId__last_name')
    Amount__sum = serializers.ReadOnlyField(source='Amount__sum')
    depositedEquityAmount = serializers.ReadOnlyField(source='Amount__sum')
    returnEquityAmount= serializers.ReadOnlyField(source='Amount__sum')
    remainingEquityAmount = serializers.ReadOnlyField(source='Amount__sum')
    #isStaff = serializers.ReadOnlyField(source='UserId.is_staff')
    class Meta:
        # Provide an association between the ModelForm and a model
        model=InvestmentActivity.objects.select_related().values('UserId__username', 'UserId__first_name', 'UserId__last_name').annotate(Sum('Amount'))
        fields = ('UserId',  'first_name', 'last_name','Amount__sum', 'depositedEquityAmount', 'returnEquityAmount','remainingEquityAmount')
    
    