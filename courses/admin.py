from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'branch', 'instructor', 'content_type', 'is_active', 'created_at')
    # Filters for branch, content type, and active status
    list_filter = ('branch', 'content_type', 'is_active')
    # Searchable fields
    search_fields = ('title', 'description')
    # Enables multi-select for enrolled learners
    filter_horizontal = ('enrolled_users',)
    # Organizing fields into sections
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'is_active', 'branch', 'instructor', 'enrolled_users')
        }),
        ('Content Details', {
            'fields': ('content_type', 'content_file'),
            'description': "Upload course content and specify the content type (SCORM, Video, or Document)."
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    # Ensure timestamps are read-only
    readonly_fields = ('created_at', 'updated_at')
