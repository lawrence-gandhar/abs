#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import *
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import sys, os

from collections import defaultdict

from app.forms import registration_forms

from app.models import *


#******************************************************************************
# HOMEPAGE
#******************************************************************************    

def check_registered_email(email=None):
    if email is not None:
        try:
            user = CustomUser.objects.filter(username__iexact = email)
            return 2
        except:
            return 1
    return 3        
     

#
#******************************************************************************
# HOMEPAGE
#******************************************************************************    

class HomeView(View):
    
    template_name = 'app/base/home.html'
    
    def get(self, request):        
        return render(request, self.template_name, {})
        

#
#******************************************************************************
# LOGIN
#******************************************************************************    

class LoginView(View):
    
    template_name = 'app/base/login.html'
    
    data = defaultdict()
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/common.js',]
    
    def get(self, request):    
        
        self.data["register_form"] = registration_forms.RegisterForm()
    
        return render(request, self.template_name, self.data)

    
    def post(self, request):
    
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    return redirect('/staff/dashboard/', permanent=True)                    
                else:
                    login(request, user)                    
                    return redirect('/dashboard/', permanent=True)
        else :
            messages.error(request, "Invalid username or password")
            return redirect('/login/', permanent=True) 

#
#******************************************************************************
#
#******************************************************************************    
        
class RegistrationView(View):
    
    template_name = 'app/base/register.html'

    data = defaultdict()
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/common.js']
     
    #
    #
    #    
    def get(self, request): 
        self.data["register_form"] = registration_forms.RegisterForm()    
        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request):
    
        email = request.POST.get("email", None)
        passwd = request.POST.get("passwd", None)
        c_passwd = request.POST.get("c_passwd", None)
        
        #
        #
        #
        
        if email is not None:
        
            chk_email = check_registered_email(email)
                            
            if chk_email == 2:
                messages.error(request, "Email is already registered")
                
            elif chk_email == 3:
                messages.error(request, "Email cannot be blank")
                
            else:
                
                user = CustomUser(email = email)
                user.set_password(passwd)
                user.is_staff = False
                user.is_superuser = False
                user.is_active = True
                user.save()
            
                register = registration_forms.RegisterForm(request.POST)
                
                if register.is_valid():
                    reg = register.save(commit=False)
                    reg.user = user
                    try: 
                        path = os.path.join(settings.MEDIA_ROOT, str(user.id))
                        os.mkdir(path, 0o777)
                        reg.save()
                    except:
                        messages.error(request, "User Creation Failed. Try again later")
                    
                    
                    return redirect("/dashboard/", permanent=False)
                    
                else:
                    messages.error(register.errors)
                    
        else:
            messages.error(request, "Email cannot be blank")    
            
            return redirect("/registration/", permanent = True)
        
        
    
