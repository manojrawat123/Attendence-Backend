from django.contrib import admin
from .models import BatchModel

# Register your models here.

@admin.register(BatchModel)
class BatchModelAdmin(admin.ModelAdmin):
    list_display = ('batch_name', 'batch_start_timing', 'batch_end_timing', 'batch_days', 'active', 'created_by', 'assigned_to', 'brand')
    list_filter = ('active', 'brand')
    search_fields = ('batch_name', 'batch_days', 'created_by__username', 'assigned_to__username')
