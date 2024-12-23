"""
URL configuration for LMS_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from users.views import role_based_redirect, home  # Import role-based redirect and home views

urlpatterns = [
    path('', home, name='home'),  # Default root path for the home page
    path('admin/', admin.site.urls),  # Admin panel
    path('users/', include('users.urls')),  # Include URLs for the users app
    path('courses/', include('courses.urls')),  # Include URLs for the courses app
    path('redirect/', role_based_redirect, name='role_based_redirect'),  # Role-based redirection
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development only if STATICFILES_DIRS is defined and not empty
if settings.DEBUG and getattr(settings, 'STATICFILES_DIRS', []):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
