from django.forms import *
from app.models import *
from django.conf import settings 

from app.constants import form_constants

import glob, os

from django.contrib.auth.forms import UserCreationForm



#******************************************************************************
# REGISTRATION FORM
#******************************************************************************    

class RegisterForm(UserCreationForm):
 
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
        
        widgets = {
            'email' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
        }
        
       

#******************************************************************************
# PROFILE PHOTO FORM
#******************************************************************************    

class ProfilePicturesForm(ModelForm):
 
    class Meta:
        model = ProfilePictures
        fields = ('picture',)
        
        widgets = {
            'picture' : FileInput(attrs = {'class':'item-img file center-block', 'required':'true', 'style':'height:0px;width:0px;margin:0px;'}),
        }
        
        
        
#******************************************************************************
# PROFILE FORM
#******************************************************************************          
       
class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('fullname','gender' ,'father_name','looking_for_gender', 'mother_name', 'religion', 'caste_creed', 'phone_number',
                  'phone_number_alternative', 'address', 'dob')
        
        MALE = 'M'
        FEMALE = 'F'
        
        gender_choices = ((MALE, 'Male'), (FEMALE, 'Female'))
        
        widgets = {
            'fullname' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'father_name' : TextInput(attrs = {'class':'form-control',}),
            'mother_name' : TextInput(attrs = {'class':'form-control',}),
            'gender' : Select(attrs = {'class':'form-control'}, choices = gender_choices),   
            'looking_for_gender' : Select(attrs = {'class':'form-control'}, choices = gender_choices),
            'religion' : Select(attrs = {'class':'form-control'}),
            'caste_creed' : Select(attrs = {'class':'form-control'}),            
            'phone_number': TextInput(attrs = {'class':'form-control',}),
            'phone_number_alternative' : TextInput(attrs = {'class':'form-control',}),
            'address' : Textarea(attrs = {'class':'form-control', 'rows':'2'}),   
            'dob': TextInput(attrs = {'class':'form-control', 'type':'date'}),
        }
        
        
        
        
        
               