from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "phone", "is_staff", "is_active",)
    list_filter = ("email", "phone", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "phone", "photo", "password")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name", "email", "phone", "photo", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email", "phone", "first_name", "last_name")
    ordering = ("first_name", "last_name", "email",)


admin.site.register(CustomUser, CustomUserAdmin)
