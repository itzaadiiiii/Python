from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'state', 'country', 'age', 'department', 'marital_status']
    list_filter = ['department', 'marital_status', 'city', 'state', 'country']
    search_fields = ['full_name', 'city', 'state', 'country']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'age', 'birthdate', 'marital_status', 'photo')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country')
        }),
        ('Work Information', {
            'fields': ('department',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
