from django.forms import *
from app.models import *
from django.conf import settings 

from app.constants import form_constants


class ProfileSearchForm(ModelForm):

    class Meta:
        model = Profile

        fields =('religion', 'caste_creed', 'aged_to', 'aged_from', 'complexion', 'qualification', 'job_details')

        widgets = {
            'religion' : Select(attrs = {'class':'form-control',}),
            'caste_creed' : Select(attrs = {'class':'form-control',}),
            'aged_to' : TextInput(attrs = {'class':'form-control', 'type':'email',}),
            'aged_from' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'complexion' : Select(attrs = {'class':'form-control',}),
            'job_details' : Select(attrs = {'class':'form-control',}),
        }