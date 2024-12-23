from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login/'), name='logout'),
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),  # Redirection URL
    path('', views.user_list, name='user_list'),  # URL for user listing
    path('dashboard/superadmin/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('dashboard/learner/', views.learner_dashboard, name='learner_dashboard'),
]

from django.urls import path
from . import views

