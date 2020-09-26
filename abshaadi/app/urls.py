from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from app.views import home, dashboard, profiles_filters, site_management
from app.views.staff import package_management, user_management

# Authorization
urlpatterns = [    
    path('',home.HomeView.as_view(), name="home"),
    path('login/', home.LoginView.as_view(template_name = 'app/base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/base/logout.html'), name = 'logout'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('registration/', home.RegistrationView.as_view(), name='registration'),
]

# Site Managers
urlpatterns += [    
    path('staff/religion-management/', never_cache(login_required(site_management.ReligionManagementView.as_view())), name='religion_management'),
    path('load_religions_into_db/', never_cache(site_management.load_religions_into_db), name="load_religions_into_db"),
    path('add_religion/', never_cache(site_management.add_religion), name="add_religion"),
    path('add_caste/', never_cache(site_management.add_caste), name="add_caste"),
    path('staff/delete_caste/<int:ins>', never_cache(site_management.delete_caste), name="delete_caste"),
    path('staff/site_managers/load_countries/', never_cache(login_required(site_management.add_countries_to_db)), name="add_countries_to_db"),
    path('get_states_dropdown/<int:id>/', never_cache(site_management.get_states_dropdown), name="get_states_dropdown"),
]


# Dashboard
urlpatterns += [    
    path('staff/dashboard/', never_cache(login_required(dashboard.StaffDashboardView.as_view())), name="staff_dashboard"),
    path('dashboard/', never_cache(login_required(dashboard.UserDashboardView.as_view())), name="dashboard"),
]


# Profile
urlpatterns += [
    path('profile/', never_cache(login_required(profiles_filters.UserProfileView.as_view())), name="user_profile"),
    path('edit/<int:id>', never_cache(login_required(profiles_filters.UserProfileEdit.as_view())), name="user_edit"),
    path('update/<int:id>', never_cache(login_required(profiles_filters.update)), name="user_update"),
    
    path('upload_profile_pic/', never_cache(login_required(profiles_filters.upload_profile_pic)), name="upload_profile_pic"),
]


# Staff
urlpatterns += [
    path('staff/package_management/view/', never_cache(login_required(package_management.PackageManagementView.as_view())), name="staff_package_management_view"),
    path('staff/user_management/users/view/', never_cache(login_required(user_management.UserManagementView.as_view())), name="user_management_view"),
    path('staff/user_management/users/delete/<int:ins>/', never_cache(login_required(user_management.delete_user)), name="delete_user"),
    path('staff/user_management/staff/view/', never_cache(login_required(user_management.StaffManagementView.as_view())), name="staff_management_view"),
    path('staff/user_management/staff/add/', never_cache(login_required(user_management.add_staff)), name="add_staff"),
]


#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
