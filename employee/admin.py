# from django.contrib import admin

# from employee.models import EmployeeUser


# class EmployeeUserAdmin(BaseUserAdmin):
#     list_display = ["email", "name", "phone", "date_of_birth", "date_of_joining", "role", "brand_name", "user_type", "is_active"]
#     fieldsets = (
#         (None, {"fields": ("email", "name", "password")}),
#         ("Permissions", {"fields": ("is_admin",  "is_active",  "user_permissions")}),
#     )
#     add_fieldsets = (
#         (None, {"fields": ("email", "name", "password1", "password2")}),
#     )
#     search_fields = ["email", "name"]
#     ordering = ["email"]
#     filter_horizontal = []


# admin.site.register(EmployeeUser, EmployeeUserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from employee.models import EmployeeUser


class EmployeeUserAdmin(BaseUserAdmin):
    list_display = ["email", "name", "phone", "date_of_birth", "date_of_joining", "role", "brand_name", "user_type", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_active", 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "name", "password1", "password2")}),
    )
    search_fields = ["email", "name"]
    ordering = ["email"]
    # Add the following line to define list_filter
    list_filter = ["is_admin", "is_active", "user_type", "brand_name"]  # Filter by these fields
    filter_horizontal = []  # Optional: filter by related models horizontally (not used here)


admin.site.register(EmployeeUser, EmployeeUserAdmin)

 