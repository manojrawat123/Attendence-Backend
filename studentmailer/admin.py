from django.contrib import admin
from .models import StudentMailer

@admin.register(StudentMailer)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'attachment', 'signature')
    search_fields = ('subject', 'body', 'signature')
    list_filter = ('attachment',)
    readonly_fields = ('attachment',)
