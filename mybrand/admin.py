from django.contrib import admin
from mybrand.models import Brand

# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'location', 'brand_email', 'service')
    search_fields = ('brand_name', 'location', 'brand_email', 'service')
