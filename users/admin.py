from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Branch

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Display these fields in the admin list view
    list_display = ['username', 'email', 'role', 'branch', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'role', 'branch']  # Add filters for quick access

    # Add 'role' and 'branch' to the editable fields when creating or editing users
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'branch')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'branch')}),
    )

    # Make 'date_joined' and 'last_login' readonly to prevent editing
    readonly_fields = ('date_joined', 'last_login')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']  # Display branch details
    search_fields = ['name']  # Add search functionality for branches
