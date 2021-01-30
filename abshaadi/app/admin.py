from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


#******************************************************************************
#
#******************************************************************************

admin.site.site_header = 'abshaadi.com'
admin.site.site_title = "Atut Bandhan Shaadi.com || Hum Bandhan Nahi Sambandh Banate Hai."

#******************************************************************************
#
#******************************************************************************

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


#******************************************************************************
#
#******************************************************************************

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    model = Religion
    list_display = ('religion_name', 'is_active',)
    ordering = ('id',)


#******************************************************************************
#
#******************************************************************************

@admin.register(Caste)
class CasteAdmin(admin.ModelAdmin):
    model = Caste
    list_display = ('religion', 'caste_name', 'is_active',)
    ordering = ('id',)


#******************************************************************************
#
#******************************************************************************

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ('package_name', 'value', 'tenure', 'tenure_types', 'description', 'created_on')
    ordering = ('id',)


#******************************************************************************
#
#******************************************************************************

@admin.register(Complexions)
class ComplexionsAdmin(admin.ModelAdmin):
    model = Complexions
    list_display = ('complexion_details', 'is_active',)
    ordering = ('id',)

#******************************************************************************
#
#******************************************************************************

@admin.register(Job_Types)
class Job_TypesAdmin(admin.ModelAdmin):
    model = Job_Types
    list_display = ('job_type', 'is_active',)
    ordering = ('id',)

#******************************************************************************
#
#******************************************************************************

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    model = Jobs
    list_display = ('job_details', 'is_active',)
    ordering = ('id',)


#******************************************************************************
#
#******************************************************************************

@admin.register(Qualifications)
class QualificationsAdmin(admin.ModelAdmin):
    model = Qualifications
    list_display = ('qualification', 'is_active',)
    ordering = ('id',)
