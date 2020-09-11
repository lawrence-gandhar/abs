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
# STAFF DASHBOARD
#******************************************************************************    

class UserManagementView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/user_management.html'

    data["page_title"] = "User Management"
    
    data["css_files"] = []
    data["js_files"] = []
    
    #
    #
    #
    
    def get(self, request):
        return render(request, self.template_name, self.data)
    
    