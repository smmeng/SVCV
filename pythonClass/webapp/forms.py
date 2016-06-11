from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator
from bootstrap3_datetime.widgets import DateTimePicker

from webapp.models import vistorType, visitorLog,employee


class visitorLogForm(forms.ModelForm):
    Type = forms.ModelChoiceField(queryset=vistorType.objects.all(),help_text="Visitor Type*:") #pnote or equity
    fname = forms.CharField(widget=forms.TextInput, help_text="First Name*:", required=True)
    lname = forms.CharField(widget=forms.TextInput, help_text="Last Name*:", required=True)
    email = forms.EmailField(widget=forms.TextInput, help_text="Email*:", required=True)
    phone = forms.CharField(widget=forms.TextInput, help_text="Phone:", required=False, 
            validators=[RegexValidator('\\+?\\(?\\d{2,4}\\)?[\\d\\s-]{3,}', message="Phone Number can't take letters")])
    employeeId= forms.ModelChoiceField(queryset=employee.objects.all(),help_text="Destination*:")
    Comments = forms.CharField(widget=forms.TextInput, help_text="Comments:", required=False)
    CreatedOn = forms.DateTimeField(
                    widget=forms.TextInput, 
                    help_text='Created On:',)

    class Meta:
        model = visitorLog
        fields = ['id','Type', 'fname', 'lname', 'email', 'phone', 'employeeId', 'Comments','CreatedOn']
