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
from app.forms import packages_forms


#******************************************************************************
# STAFF DASHBOARD
#******************************************************************************    

class PackageManagementView(View):

    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/package_management.html'

    data["page_title"] = "Package Management"
    
    data["css_files"] = []
    data["js_files"] = []
    
    #
    #
    #
    
    def get(self, request):
    
        self.data["packages"] = Package.objects.all()
        
        self.data["add_package_form"] = packages_forms.AddPackageForm()
        
        return render(request, self.template_name, self.data)
    
    def post(self, request):
        add_package_form = packages_forms.AddPackageForm(request.POST)

        if add_package_form.is_valid():
            inc = add_package_form.save(commit=False)
            inc.user = request.user
            inc.save()       
        else:
            print(add_package_form.errors.as_data())
        return redirect('/staff/package_management/view/', self.data)
