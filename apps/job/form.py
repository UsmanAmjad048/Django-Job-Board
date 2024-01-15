from django import forms
from .models import Job, Application


class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'short_description', 'long_description', 'company_name', 'company_address',
                  'company_zipcode', 'company_place', 'company_country', 'company_size',]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email','age','language', 'education',
                  'content', 'location', 'experience', 'cv_file']
