from django.contrib import admin
from .models import Appointment, TimeSlot, Availablity
from apps.profile.models import User, Doctor

# Register your models here.


class TimeSlotInline(admin.TabularInline):
    model = Availablity.time_slot.through


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = Doctor.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ["js/time-shortcuts.js"]


@admin.register(Availablity)
class AvailabilityAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = Doctor.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    inlines = [TimeSlotInline]
    list_display = ["date", "doctor"]


admin.site.register(TimeSlot)
