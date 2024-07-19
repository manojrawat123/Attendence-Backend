from django.contrib import admin
from studentattendence.models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'batch_id', 'attendance_status')
    list_filter = ('attendance_status', 'date', 'batch_id')
    search_fields = ('student__name', 'batch_id__name')
    ordering = ('-date',)

    # Optional: Add any additional customizations like inlines, fieldsets, etc.
    # If you have more fields to show in the change view, you can customize it here.

# Alternatively, you can register without the decorator
# admin.site.register(Attendance, AttendanceAdmin)
