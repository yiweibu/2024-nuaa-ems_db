from django.contrib import admin
# Register your models here.
from .models import Employee

'''
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'name', 'gender', 'age', 'phone', 'position', 'department_name', 'total_salary', 'is_active', 'is_staff', 'is_admin', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'position', 'department_name')
    search_fields = ('email', 'id', 'name', 'gender', 'phone', 'position', 'department_name')
    ordering = ('email',)
    actions = ['make_admin', 'remove_admin', 'make_superuser', 'remove_superuser']

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

    def remove_admin(self, request, queryset):
        queryset.update(is_admin=False)

    def make_superuser(self, request, queryset):
        queryset.update(is_superuser=True)

    def remove_superuser(self, request, queryset):
        queryset.update(is_superuser=False)
'''