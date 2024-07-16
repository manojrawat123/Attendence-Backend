from django.contrib import admin
from .models import Student  # Import the Student model from the current app

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'batch_id', 'student_phone', 'student_email', 'added_by', 'active', 'gender')
    search_fields = ('student_name', 'student_email', 'batch_id__batch_name')
    list_filter = ('batch_id', 'active', 'gender') 

admin.site.register(Student, StudentAdmin)
