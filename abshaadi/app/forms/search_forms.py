from django.forms import *
from app.models import *
from django.conf import settings

from app.constants import form_constants


class ProfileSearchForm(ModelForm):

    class Meta:
        model = Profile

        fields =('religion', 'caste_creed', 'complexion', 'qualification', 'job_details', 'country', 'state', 'city', 'job_type')

        widgets = {
            'religion' : Select(attrs = {'class':'form-control selectpicker religion_select', 'multiple':'true'}),
            'caste_creed' : Select(attrs = {'class':'form-control selectpicker castes_select', 'multiple':'true'}),
            'complexion' : Select(attrs = {'class':'form-control ', 'multiple':'true'}),
            'qualification' : TextInput(attrs = {'class':'form-control', }),
            'job_type' : Select(attrs = {'class':'form-control',}),
            'job_details' : TextInput(attrs = {'class':'form-control',}),
            'country' : Select(attrs = {'class':'form-control selectpicker country_select', 'data-live-search':'true' ,'multiple':'true'}),
            'state' : Select(attrs = {'class':'form-control states_select selectpicker', 'data-live-search':'true' , 'multiple':'true',}),
            'city' : Select(attrs = {'class':'form-control selectpicker city_select', 'data-live-search':'true' ,'multiple':'true'}),
        }

#
#
#


class MyFiltersForm(ModelForm):

    class Meta:
        model = MyFilters

        fields = ( 'aged_to', 'aged_from', 'l_cities', 'l_states', 'l_countries', 'l_religions', 'l_caste', 'l_qualifications', 'l_jobs', 'l_complexions', 'job_type')

        widgets = {
            'l_religions' : Select(attrs = {'class':'form-control selectpicker religion_select', 'multiple':'true'}),
            'l_cities' : Select(attrs = {'class':'form-control selectpicker city_select', 'multiple':'true'}),
            'l_states' : Select(attrs = {'class':'form-control selectpicker states_select', 'multiple':'true'}),
            'l_countries' : Select(attrs = {'class':'form-control selectpicker country_select', 'multiple':'true'}),
            'l_caste' : Select(attrs = {'class':'form-control selectpicker castes_select', 'multiple':'true'}),
            'l_qualifications' : Select(attrs = {'class':'form-control selectpicker qualification_select', 'data-live-search':'true' ,'multiple':'true'}),
            'job_type' : Select(attrs = {'class':'form-control selectpicker castes_select', 'multiple':'true'}),
            'l_jobs' : Select(attrs = {'class':'form-control selectpicker jobs_select', 'data-live-search':'true' ,'multiple':'true'}),
            'l_complexions' : Select(attrs = {'class':'form-control selectpicker', 'data-live-search':'true' ,'multiple':'true'}),
            'aged_to' : TextInput(attrs = {'class':'form-control hide', }),
            'aged_from' : TextInput(attrs = {'class':'form-control hide', }),
        }

#
#
#

class PartnerProfileForm(ModelForm):

    class Meta:
        model = Partner_Preferences

        fields = ( 'aged_to', 'aged_from', 'l_cities', 'l_states', 'l_countries', 'l_religions', 'l_caste', 'l_qualifications', 'l_jobs', 'l_complexions', 'job_type')

        widgets = {
            'l_religions' : Select(attrs = {'class':'form-control selectpicker religion_select', 'multiple':'true'}),
            'l_cities' : Select(attrs = {'class':'form-control selectpicker city_select', 'multiple':'true'}),
            'l_states' : Select(attrs = {'class':'form-control selectpicker states_select', 'multiple':'true'}),
            'l_countries' : Select(attrs = {'class':'form-control selectpicker country_select', 'multiple':'true'}),
            'l_caste' : Select(attrs = {'class':'form-control selectpicker castes_select', 'multiple':'true'}),
            'l_qualifications' : Select(attrs = {'class':'form-control selectpicker qualification_select', 'multiple':'true'}),
            'job_type' : Select(attrs = {'class':'form-control selectpicker castes_select', 'multiple':'true'}),
            'l_jobs' : Select(attrs = {'class':'form-control selectpicker jobs_select', 'multiple':'true'}),
            'l_complexions' : Select(attrs = {'class':'form-control selectpicker', 'multiple':'true'}),
            'aged_to' : TextInput(attrs = {'class':'form-control hide', }),
            'aged_from' : TextInput(attrs = {'class':'form-control hide', }),
        }
