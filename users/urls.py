from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # User authentication routes
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login/'), name='logout'),

    # Role-based redirection
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),

    # User-related views
    path('', views.user_list, name='user_list'),

    # Dashboard views for each role
    path('dashboard/superadmin/', views.super_admin_dashboard, name='dashboard_superadmin'),
    path('dashboard/admin/', views.admin_dashboard, name='dashboard_admin'),
    path('dashboard/instructor/', views.instructor_dashboard, name='dashboard_instructor'),
    path('dashboard/learner/', views.learner_dashboard, name='dashboard_learner'),
]
