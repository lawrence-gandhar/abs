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

from django.utils import safestring

import json

#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   

class UserProfileView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/users/profile.html'

    data["page_title"] = "My Profile"
    
    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js', 'custom_files/js/common.js', 'custom_files/js/profile_management.js']
    
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
        
        self.data["edit_form"] = ProfileForm(instance=self.data["profile"])
        
        return render(request, self.template_name, self.data)


#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   

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


#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   
        
def update(request,id):
    if request.method=='POST':
        form = RegisterForm(request.POST) 
        form1 = ProfileForm(request.POST)
        
        
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
    
    
#******************************************************************************
# EDIT PROFILE
#****************************************************************************** 
    
def edit_personal_info(request):
    if request.POST:
       
        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return redirect('/page_403/') 

        pers_info = ProfileForm(request.POST, instance=profile)
        
        if pers_info.is_valid():
            pers_info.save()            
        else:
            print(pers_info.errors)
        
        return redirect('/profile/')
    return redirect('/page_403/')        
    

#******************************************************************************
# SEARCH FILTER SAVE
#******************************************************************************  

def save_partner_preferences(request):
    
    if request.POST:
        form = search_forms.MyFiltersForm(request.POST)
        
        inp = request.POST.get("inp", None)
        
        if inp is not None:
        
            if form.is_valid():
                ins = form.save(commit=False)
                ins.filter_name = inp
                ins.user = request.user
                ins.save()
                return HttpResponse(json.dumps({'code':'1', 'error':''}))
            else:
                return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(form.errors)}))
        else:
            return HttpResponse(json.dumps({'code':'0', 'error':'Filter Name is required'}))
    return HttpResponse(json.dumps({'code':'0', 'error':'Invalid Operation'}))
    
     
#******************************************************************************
# SEARCH FILTERS
#******************************************************************************    

class MySearchView(View):

    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/users/search_results.html'

    data["page_title"] = "Ratner Profile Search"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/common.js',]
    
    #
    #
    #
    
    def get(self, request):
        self.data["search_profile"] = search_forms.MyFiltersForm()
        return render(request, self.template_name, self.data)
    
    #
    #
    #
    
    def post(self, request):
        self.data["search_profile"] = search_forms.MyFiltersForm(request.POST)

        if self.data["search_profile"].is_valid():
            pass
        return render(request, self.template_name, self.data)
  
  
  

    