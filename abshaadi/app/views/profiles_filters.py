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


#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************   

class UserProfileView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/users/profile.html'

    data["page_title"] = "My Profile"
    
    data["css_files"] = []
    data["js_files"] = []
    
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
        
        
        return render(request, self.template_name, self.data)
        
        

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
    
    
    
    