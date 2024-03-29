from django.contrib import admin
from brand.models import Branch

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch_name', 'location', 'branch_email', 'service']
    search_fields = ['branch_name', 'location']

admin.site.register(Branch, BranchAdmin)