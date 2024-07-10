from django.contrib import admin
from .models import EmailTemplate

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'subject', 'signature')
    search_fields = ('template_name', 'subject', 'template_body')
    list_filter = ('template_name',)

admin.site.register(EmailTemplate, EmailTemplateAdmin)