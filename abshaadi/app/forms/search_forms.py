from django.forms import *
from app.models import *
from django.conf import settings 

from app.constants import form_constants


class ProfileSearchForm(ModelForm):

    class Meta:
        model = Profile

        fields =('religion', 'caste_creed', 'aged_to', 'aged_from', 'complexion', 'qualification', 'job_details', 'country', 'state', 'city')

        widgets = {
            'religion' : Select(attrs = {'class':'form-control selectpicker',}),
            'caste_creed' : Select(attrs = {'class':'form-control selectpicker',}),
            'aged_to' : TextInput(attrs = {'class':'form-control', }),
            'aged_from' : TextInput(attrs = {'class':'form-control', }),
            'complexion' : Select(attrs = {'class':'form-control',}),
            'qualification' : TextInput(attrs = {'class':'form-control', }),
            'job_details' : TextInput(attrs = {'class':'form-control',}),
            'country' : Select(attrs = {'class':'form-control selectpicker', 'onchange':'get_states_dropdown($(this))'}),
            'state' : Select(attrs = {'class':'form-control states_select', 'multiple':'true', 'data-actions-box':'true'}),
            'city' : Select(attrs = {'class':'form-control', 'multiple':'true'}),
        }