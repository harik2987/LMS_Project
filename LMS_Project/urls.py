from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import role_based_redirect, home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('redirect/', role_based_redirect, name='role_based_redirect'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    # Safely get the first STATICFILES_DIRS entry if it exists
    static_root = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None
    if static_root:
        urlpatterns += static(settings.STATIC_URL, document_root=static_root)
