from django.contrib import admin
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
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    list_display_links = ["email"]
    model = User
    inlines = [ContactInline]
    exclude = (
        "last_login",
        "groups",
        "user_permissions",
        "is_active",
        "is_staff",
        "date_joined",
        "is_superuser",
    )
    list_filter = ["username", "email"]
    search_fields = ["username"]


# admin.site.register(Availablity)
