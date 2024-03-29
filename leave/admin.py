from leave.models import Leave  
from django.contrib import admin


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee_user', 'date']
    list_filter = ['employee_user']
    search_fields = ['employee_user__name', 'employee_user__email']

admin.site.register(Leave, LeaveAdmin)
