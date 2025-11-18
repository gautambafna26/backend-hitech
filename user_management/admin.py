from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("address",)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("address",)}),
    )
