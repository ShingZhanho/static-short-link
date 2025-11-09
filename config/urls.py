"""
URL configuration for j-shi.ng project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    # Root redirect to login/portal
    path('', RedirectView.as_view(url='/auth/login/', permanent=False), name='home'),
    
    # Authentication
    path('auth/login/', auth_views.LoginView.as_view(
        template_name='shortener/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Django admin (backup access)
    path('django-admin/', admin.site.urls),
    
    # Shortener app URLs
    path('', include('shortener.urls')),
]
