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
import sys, os, json, hashlib

from django.utils import safestring

from django.contrib.auth.hashers import make_password

from collections import defaultdict

from app.forms.registration_forms import RegisterForm

from app.models import *

from app.helpers import *

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

#******************************************************************************
# LOGOUT SIGNALS
#******************************************************************************


@receiver(user_logged_out)
def post_login(sender, user, request, **kwargs):
    cus = CustomUser.objects.get(pk = request.user.id)
    cus.online_now = False
    cus.save()


#******************************************************************************
# 403 Page
#******************************************************************************

def page_403(request):
    return render(request, 'app/base/403_error.html')


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
    data = defaultdict()

    def get(self, request):

        self.data["register_form"] = RegisterForm()

        return render(request, self.template_name, self.data)


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

        self.data["register_form"] = RegisterForm()

        return render(request, self.template_name, self.data)


    def post(self, request):

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                cus = CustomUser.objects.get(pk = user.id)
                cus.online_now = True
                cus.save()

                return HttpResponse('1')
        else:
            return HttpResponse('Invalid username or password')


#
#******************************************************************************
#
#******************************************************************************

def my_redirect_page(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect('/staff/dashboard/', permanent=True)
    else:
        return redirect('/dashboard/', permanent=True)



#
#******************************************************************************
#
#******************************************************************************

def register_form(request):
    if request.POST:

        email = request.POST.get('email', None)
        #
        #
        #

        if email is not None:
            reg_form = RegisterForm(request.POST)

            chk_email = check_registered_email(email)

            if chk_email == 2:
                return HttpResponse("Email is already registered")

            elif chk_email == 3:
                return HttpResponse("Email cannot be blank")
            else:

                if reg_form.is_valid():
                    reg = reg_form.save(commit=False)
                    reg.is_staff = False
                    reg.is_superuser = False

                    reg.save()

                    path = os.path.join(settings.MEDIA_ROOT, str(reg.id))
                    os.mkdir(path, 0o777)

                    profile = Profile(
                        user = reg
                    )

                    profile.save()

                    #
                    # Send confirmation email
                    #


                    user = CustomUser.objects.get(email = email)
                    profile = Profile.objects.get(user_id = user.pk)
                    uid = profile.uid

                    hashstr = uid+"<_secret_>"+settings.SECRET_KEY
                    hashstr = hashlib.sha384(hashstr.encode())
                    hashstr = hashstr.hexdigest()

                    conf_email = ConfirmEmail(
                        user = user,
                        key = hashstr
                    )

                    conf_email.save()

                    send_email_from_app(email, uid, hashstr, template = 'app/users/welcome.html')

                    return HttpResponse(json.dumps({'code':'1', 'error':''}))

                else:
                    return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(reg_form.errors)}))

        else:
            return HttpResponse("Email cannot be blank")

#======================================================================
# Change Password
#======================================================================
#

def change_password(request):
    if request.POST:
        if validate_password(request.POST["password1"]):
            request.user.set_password(request.POST["password1"])
            update_session_auth_hash(request, request.user)
            request.user.save()
            return HttpResponse("Password Changed Successfully")
        return HttpResponse('This password must contain at least 8 characters.')
    return HttpResponse(0)


#======================================================================
# Validate Password
#======================================================================
#

def validate_password(password):
    if len(password) < 8:
        return False
    return True


#
#
#

def confirmemail(request, qstr = None):
    print('hello')
    if qstr is not None:
        # try:
        customer = ConfirmEmail.objects.get(key = qstr)
        

        # update CustomUser

        user = CustomUser.objects.get(pk = customer.user_id)
        user.email_verified  =  True
        user.subscribe_email = True
        user.save()

        # Delete from confirmemail

        customer.delete()

        # except:
        #     pass

    return redirect("/login/")
