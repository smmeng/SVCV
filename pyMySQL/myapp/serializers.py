from rest_framework import serializers
from myapp.models import InvestmentActivity, PROJECT, UserProfile #Vendor, Company, Status,  
from django.contrib.auth.models import   User

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
        
    
class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    ProjectId_id = serializers.ReadOnlyField(source='ProjectId.ProjectName')
    ProjectStatus = serializers.ReadOnlyField(source='ProjectId.Status.Status')
    UserId_id = serializers.ReadOnlyField(source='UserId.username')
    Type  = serializers.ReadOnlyField(source='Type.Type')

    #paginate_by = 10
    print 'ActivitySerializer'
    
    class Meta:
    # Provide an association between the ModelForm and a model
    
        model = InvestmentActivity
        fields = ('ActivityId','UserId_id', 'Type','ProjectId_id', 'ProjectStatus', 'Date', 'Memo', 'Amount', 'CreatedOn')
    