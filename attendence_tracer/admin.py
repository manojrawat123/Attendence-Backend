from attendence_tracer.models import Attendence
from django.contrib import admin


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee_user', 'check_in_time', 'check_out_time', 'date']
    list_filter = ['employee_user', "date"]
    search_fields = ['employee_user__name', 'employee_user__email', "date"]

admin.site.register(Attendence, AttendanceAdmin)
