from django.contrib import admin
from employee.models import EmployeeUser

# Register your models here.
class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone', 'date_of_birth', 'date_of_joining', 'role', 'user_type', 'is_active']
    search_fields = ['email', 'name', 'phone']
    list_filter = ['is_active', 'user_type', 'date_of_joining']

admin.site.register(EmployeeUser, EmployeeUserAdmin)
