from django import forms
from decimal import Decimal

from django.utils import timezone

from myapp.models import PROJECT, Vendor, Company, Status, UserProfile, TransactionType, InvestmentActivity

class ProjectForm(forms.ModelForm):
    ProjectId = forms.IntegerField(widget=forms.HiddenInput)
    ProjectName = forms.CharField(widget=forms.TextInput,  help_text="Project Name*:")
    DESCRIPTION = forms.CharField(widget=forms.Textarea,help_text="Project Description:")
    SinglePhase = forms.BooleanField(widget=forms.CheckboxInput,help_text="Single Phase Project?")
    Allocation = forms.FloatField(widget=forms.NumberInput,help_text="Total Allocation:")
    Committed = forms.DecimalField(widget=forms.NumberInput,help_text="Total Commitment:")
    CompanyId = forms.ModelChoiceField(queryset=Company.objects.all(),help_text="Company:")
    VendorId = forms.ModelChoiceField(queryset=Vendor.objects.all(),help_text="Vendor:")
    Status = forms.ModelChoiceField(queryset=Status.objects.all(),help_text="Project Status:")
    StartDate = forms.DateField(widget=forms.DateInput, initial=timezone.now(), help_text="Start Date*:")
    EndDate = forms.DateField(widget=forms.DateInput, initial=timezone.now(), help_text="Target Completion Date:")
    
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = PROJECT
        fields = ('ProjectId', 'ProjectName','DESCRIPTION', 'SinglePhase', 'Allocation', 'Committed', 'CompanyId', 'VendorId', 'Status', 'StartDate', 'EndDate')

class InvestmentActivityForm(forms.ModelForm):
    UserId =forms.ModelChoiceField(queryset=UserProfile.objects.all(),help_text="Name:")
    Type_id = forms.ModelChoiceField(queryset=TransactionType.objects.all())
    Date = forms.DateField(widget=forms.DateInput)
    ProjectId = forms.IntegerField(widget=forms.TextInput)
    Memo = forms.CharField(widget=forms.TextInput)
    Amount = forms.DecimalField(widget=forms.NumberInput)
    Status = forms.ModelChoiceField(queryset=Status.objects.all())
    CompanyId = forms.ModelChoiceField(queryset=Company.objects.all())
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = InvestmentActivity
        fields = ('UserId',)