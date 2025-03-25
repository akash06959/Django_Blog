"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

def redirect_to_blog(request):
    return redirect('post_list')

# Basic URL patterns
urlpatterns = [
    path('', redirect_to_blog, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
]

# Serve media and static files for both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Use the first entry in STATICFILES_DIRS if it exists, otherwise fallback to settings.STATIC_ROOT
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)

# Also add explicit media file serving path
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT}),
]
