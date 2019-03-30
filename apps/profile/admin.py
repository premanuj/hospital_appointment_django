from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Patient, Contact
from apps.appointment.models import Availablity
from django.db import models
from django import forms

# Register your models here.


class ContactInline(admin.TabularInline):
    model = Contact


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ["user", "department", "time_slot", "education"]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ["user"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "date_of_birth", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("date_of_birth", "first_name", "last_name", "gender")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "role"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)
    filter_horizontal = ()


# admin.site.register(Availablity)
