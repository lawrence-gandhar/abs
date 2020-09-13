#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.conf import settings
from app.models import * 
from app.forms import *


#******************************************************************************
# USER MANAGEMENT VIEW
#******************************************************************************    

class UserManagementView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/user_management.html'

    data["page_title"] = "User Management"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/user_management.js']
    
    #
    #
    #
    
    def get(self, request):
        
        self.data["users"] = Profile.objects.all()
        
        return render(request, self.template_name, self.data)
   


#******************************************************************************
# STAFF MANAGEMENT VIEW
#******************************************************************************    

class StaffManagementView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/staff_management.html'

    data["page_title"] = "User Management"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/user_management.js']
    
    #
    #
    #
    
    def get(self, request):
        
        self.data["users"] = CustomUser.objects.filter(is_staff = True)
        
        return render(request, self.template_name, self.data)
   
    
#******************************************************************************
# DELETE USER
#******************************************************************************    
    
def delete_user(request, ins=None):
    
    if ins is not None:
       
        try:
            CustomUser.objects.get(pk = ins).delete()
            return HttpResponse('1')
        except:
            return HttpResponse('2')
        
    return HttpResponse('0')
    