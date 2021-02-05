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
from app.forms import registration_forms, search_forms


#******************************************************************************
# STAFF DASHBOARD
#******************************************************************************

class StaffDashboardView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/staff/index.html'

    data["page_title"] = "Staff Dashboard"

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/packages_counter.js']

    #
    #
    #

    def get(self, request):

        self.data["packages"] = Package.objects.all().order_by("is_active")

        return render(request, self.template_name, self.data)


#******************************************************************************
# USER DASHBOARD
#******************************************************************************

class UserDashboardView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/users/index.html'

    data["page_title"] = "User Dashboard"

    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js',
                        'custom_files/js/search_filters.js', 'custom_files/js/image_crop.js', 'custom_files/js/partner_preferences.js']

    #
    #
    #

    def get(self, request):

        self.data["packages"] = Package.objects.filter(is_active = True)

        self.data["profile_picture"] = registration_forms.ProfilePicturesForm()
        self.data["redirect_url"] = request.get_full_path()

        try:
            xx = ProfilePictures.objects.get(user = request.user, set_as_profile_pic = True)
            self.data["pro_pic"] = xx.picture
        except:
            self.data["pro_pic"] = None

        try:
            pp = Partner_Preferences.objects.get(user = request.user)
            self.data["partner_preference"] = search_forms.PartnerProfileForm(auto_id = 'id_for_pref_%s', instance = pp)
        except:
            self.data["partner_preference"] = search_forms.PartnerProfileForm(auto_id = 'id_for_pref_%s')


        self.data["search_profile"] = search_forms.MyFiltersForm()


        return render(request, self.template_name, self.data)
