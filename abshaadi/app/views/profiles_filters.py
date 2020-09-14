#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict

from app.models import * 
from app.forms import *
from django.shortcuts import get_object_or_404
from app.forms.registration_forms import RegisterForm,ProfileForm
from django.http import Http404

#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   

class UserProfileView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/users/profile.html'

    data["page_title"] = "My Profile"
    
    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js', 'custom_files/js/common.js']
    
    #
    #
    #
    
    def get(self, request):
        
        try:
            profile_pic = ProfilePictures.objects.get(user=request.user, set_as_profile_pic=True)
            pro_pic = profile_pic.picture
            
        except:
            pro_pic = ""
            pass
        
        self.data["pro_pic"] = pro_pic
        self.data["profile"] = Profile.objects.get(user=request.user)        
        self.data["gallery"] = ProfilePictures.objects.filter(user=request.user, set_as_profile_pic=False)
        self.data['abc']=1
        
        
        return render(request, self.template_name, self.data)

class UserProfileEdit(View):
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/users/profile.html'
    

    data["page_title"] = "My Profile"
    
    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js', 'custom_files/js/common.js']
    
    def get(self,request,id):
        try:
            profile_pic = ProfilePictures.objects.get(user=request.user, set_as_profile_pic=True)
            pro_pic = profile_pic.picture
            
        except:
            pro_pic = ""
            pass
        
        self.data["pro_pic"] = pro_pic
        self.data["profile"] = Profile.objects.get(user=request.user)        
        self.data["gallery"] = ProfilePictures.objects.filter(user=request.user, set_as_profile_pic=False)
        
        self.data['profile'] = Profile.objects.get(id=id)
        
        # print(profile.user)  
        return render(request,self.template_name,self.data)


        
def update(request,id):
    if request.method=='POST':
        form =RegisterForm(request.POST) 
        form1 =ProfileForm(request.POST)
        # print(form1['father_name'].value())
        obj = Profile.objects.get(id=id)
        obj.fullname = form['fullname'].value()
        obj.gender = form['gender'].value()
        obj.looking_for_gender = form['looking_for_gender'].value()
        obj.aged_from = form['aged_from'].value()
        obj.aged_to = form['aged_to'].value()
        obj.father_name=form1['father_name'].value()
        obj.mother_name = form1['mother_name'].value()
        obj.dob = form1['dob'].value()
        obj.religion_id = form1['religion'].value()
        obj.caste_creed_id = form1['caste_creed'].value()
        obj.save()
        return redirect('/profile')
    
    return render(request,'app/users/profile.html',{'profile':form1})

#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   

def upload_profile_pic(request):
    
    if request.method == 'POST' and request.FILES['picture']:
        
        files = request.FILES
        
        ProfilePictures.objects.filter(user = request.user).update(set_as_profile_pic = False)
                
        profile_pic = ProfilePictures(
                picture = request.FILES['picture'],
                user = request.user,
                set_as_profile_pic = True,
            )
        
        profile_pic.save()
        
        return HttpResponse('1')
    
    
    
    