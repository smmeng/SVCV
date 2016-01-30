from rest_framework import serializers
from myapp.models import InvestmentActivity, PROJECT, TransactionType #,Vendor, Company, Status, UserProfile, 
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
    Type = serializers.ReadOnlyField(source='Type.Description')
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
        fields = ('UserId', 'first_name', 'last_name', 'Type', 'ProjectId', 'Amount', 'CreatedOn')
        
        
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = PROJECT
        fields = ('ProjectId', 'ProjectName', 'DESCRIPTION', 'Committed', 'VendorId', 'CompanyId', 'Status')