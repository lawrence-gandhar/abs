from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from app.views import home, dashboard, profiles_filters
from app.views.staff import package_management

# Authorization
urlpatterns = [    
    path('',home.HomeView.as_view(), name="home"),
    path('login/', home.LoginView.as_view(template_name = 'app/base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/base/logout.html'), name = 'logout'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('registration/', home.RegistrationView.as_view(), name='registration'),
]  

# Dashboard
urlpatterns += [    
    path('staff/dashboard/', never_cache(login_required(dashboard.StaffDashboardView.as_view())), name="staff_dashboard"),
    path('dashboard/', never_cache(login_required(dashboard.UserDashboardView.as_view())), name="dashboard"),
]

# Profile
urlpatterns += [
    path('profile/', never_cache(login_required(profiles_filters.UserProfileView.as_view())), name="user_profile"),
    path('upload_profile_pic/', never_cache(login_required(profiles_filters.upload_profile_pic)), name="upload_profile_pic"),
]

# Package
urlpatterns += [
    path('staff/package_management/view/', never_cache(login_required(package_management.PackageManagementView.as_view())), name="staff_package_management_view"),
    path('staff/edit_package_management/', never_cache(login_required(package_management.edit_package_management)), name="edit_package_management"),
    path('staff/delete_package_management/<int:ins>/', never_cache(login_required(package_management.delete_package_management)), name="delete_package_management"),
]

#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
