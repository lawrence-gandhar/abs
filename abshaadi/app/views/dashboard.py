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

from app.helpers import *

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

        users = CustomUser.objects.filter(is_superuser = False, is_staff = False).values_list('id', flat = True)

        self.data["registered_users"] = users.count()
        self.data["active_users"] = users.filter(is_active = True).count()
        self.data["inactive_users"] = users.filter(is_active = False).count()

        profiles = Profile.objects.filter(user__in = list(users))
        self.data["female"] = profiles.filter(gender = 'F').count()
        self.data["male"] = profiles.filter(gender = 'M').count()

        self.data["premium_users"] = PaidUser.objects.filter(user__in = list(users), is_active = True).count()


        print(self.data)


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
        self.data["search_profile"] = search_forms.MyFiltersForm()

        self.data["redirect_url"] = request.get_full_path()

        try:
            xx = ProfilePictures.objects.get(user = request.user, set_as_profile_pic = True)
            self.data["pro_pic"] = xx.picture
        except:
            self.data["pro_pic"] = None


        aged_to = None
        aged_from = 18

        profile = Profile.objects.get(user = request.user)

        l_religions = []
        l_countries = []
        l_caste = []
        l_cities = []
        l_states = []
        l_caste_main = []

        try:
            pp = Partner_Preferences.objects.get(user = request.user)
            self.data["partner_preference"] = search_forms.PartnerProfileForm(auto_id = 'id_for_pref_%s', instance = pp)

            #
            #
            self.data["job_type"] = pp.job_type.all()
            self.data["l_cities"] = pp.l_cities.all()
            self.data["l_countries"] = pp.l_countries.all()
            self.data["l_states"] = pp.l_states.all()
            self.data["l_religions"] = pp.l_religions.all()
            self.data["l_caste"] = pp.l_caste.all()

            l_religions = pp.l_religions.all()
            l_countries = pp.l_countries.all()
            l_caste = pp.l_caste.all()
            l_cities = pp.l_cities.all()
            l_states = pp.l_states.all()


            l_caste_main = []
            for caste in l_caste:
                if caste.id > 1:
                    l_caste_main = caste

            aged_to = pp.aged_to
            aged_from = pp.aged_from

        except:
            self.data["partner_preference"] = search_forms.PartnerProfileForm(auto_id = 'id_for_pref_%s')

            self.data["job_type"] = []
            self.data["l_cities"] = []
            self.data["l_countries"] = []
            self.data["l_states"] = []


        search = Profile.objects.filter(gender = profile.looking_for_gender, user__is_active = True)

        if aged_to is not None:
            search = search.filter(dob__lte = get_birth_full_from_age(aged_to))

        if aged_from is not None:
            search = search.filter(dob__gte = get_birth_full_from_age(aged_from))


        if len(l_religions) > 0:
            rel = Religion.objects.filter(pk__in = l_religions).values_list('id', flat = True)

            search = search.filter(religion_id__in = list(rel))

        if len(l_caste_main) > 0:
            castes = Caste.objects.filter(pk__in = l_caste_main).values_list('id', flat = True)
            search = search.filter(caste_creed_id__in = list(castes))

        if len(l_countries) > 0:
            countries = Countries.objects.filter(pk__in = l_countries).values_list('id', flat=True)
            search = search.filter(country__in = list(countries))

        search = search.values()

        search_res = []

        profile_like = ProfileLike.objects.filter(by_user = request.user).values_list('user_id', flat = True)

        for row in search:

            row['age'] = get_age_from_dob(row['dob'].strftime("%Y-%m-%d"), True)

            if row["id"] not in profile_like:
                row["profile_counter"] = False
            else:
                row["profile_counter"] = True
            search_res.append(row)

        for i in range(len(search_res)):
            coun = search_res[i]['country_id']
            city = search_res[i]['city_id']

            city = Countries_Cities.objects.get(pk=city)
            country = Countries.objects.get(pk=coun)

            search_res[i]['city']=city.city_name
            search_res[i]['country']=country

        self.data["search_results"] = search_res



        #
        #
        #




        return render(request, self.template_name, self.data)
