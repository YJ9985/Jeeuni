# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'provider')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'provider', 'is_staff')

admin.site.register(User, CustomUserAdmin)
