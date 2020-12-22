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
from app.forms import user_management_forms

import json

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
        self.data["user_edit_form"] = user_management_forms.StaffUserEditForm()
        return render(request, self.template_name, self.data)

    #
    #
    #

    def post(self, request):

        user_id = request.POST.get("user_id", None)

        try:
            user = CustomUser.objects.get(pk = int(user_id))

            profile = Profile.objects.get(user = user)
            user_edit_form = user_management_forms.StaffUserEditForm(request.POST, instance = profile)

            if user_edit_form.is_valid():
                user_edit_form.save()

        except:
            pass
        
        if request.method=="POST":
            id=request.POST.getlist('id[]')
            print(id)
            for i in id:
                cus= CustomUser.objects.get(pk=i)
                cus.delete()
        return redirect("user_management_view")



#******************************************************************************
# FETCH USER DETAILS
#******************************************************************************

def fetch_user_details(request):
    if request.POST:

        user_json = {}

        try:
            user = CustomUser.objects.get(pk = int(request.POST["user_id"]))

            profile = Profile.objects.get(user = user)

            user_json["phone_number"] = profile.phone_number
            user_json["fullname"] = profile.fullname
            user_json["phone_number_alternative"] = profile.phone_number_alternative
            user_json["package"] = profile.package
            user_json["assigned_to"] = profile.assigned_to.id

        except:
            pass

        return HttpResponse(json.dumps(user_json))
    return HttpResponse(0)




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
        self.data["add_user_form"] = user_management_forms.CreateUserForm(auto_id="form_%s")

        return render(request, self.template_name, self.data)


#******************************************************************************
# ADD USER
#******************************************************************************

def add_staff(request):
    if request.POST:
        add_staff = user_management_forms.CreateUserForm(request.POST, auto_id="form_%s")

        if add_staff.is_valid():
            add_staff.save(commit = False)
            add_staff.is_satff = True
            add_staff.save()
            return HttpResponse('1')
        else:
            return HttpResponse(add_staff.errors)
    return HttpResponse('0')




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


#******************************************************************************
# USER PROFILE
#******************************************************************************

def user_profile_view(request, user_id=None):
    # print(user_id)

    if user_id is not None:

        template_name = 'app/base/base.html'

        data = defaultdict()

        data["included_template"] = 'app/staff/user_profile.html'

        data["page_title"] = "User Profile"

        data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
        data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/site_management.js',
                        'custom_files/js/common.js']

        try:
            user = CustomUser.objects.get(pk = user_id)
        except:
            return redirect('/page_403/')

        data["my_profile"] = Profile.objects.get(user = user)

        try:
            data["my_profile_pic"] = ProfilePictures.objects.get(user = user, set_as_profile_pic = True)
        except:
            data["my_profile_pic"] = None

        data["gallery"] = ProfilePictures.objects.filter(user=user, set_as_profile_pic=False)

        return render(request, template_name, data)

    return redirect('/page_403/')


def upload_profile_pic(request,id):
    print(id)
    # print(request.build_absolute_uri())
    if request.method == 'POST' and request.FILES['picture']:
        files = request.FILES
        # print(request.user)
        # to_user_id = request.POST.get('to_user_id', None)
        
        ProfilePictures.objects.filter(user_id = id).delete()

        profile_pic = ProfilePictures(
                picture = request.FILES['picture'],
                user_id = id,
                set_as_profile_pic = False,
            )

        profile_pic.save()

        return HttpResponse('1')