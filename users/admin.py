from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser", "is_active")
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")


