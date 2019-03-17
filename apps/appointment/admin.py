from django.contrib import admin
from .models import Appointment, TimeSlot, Availablity
from apps.profile.models import User, Doctor

# Register your models here.


class TimeSlotInline(admin.TabularInline):
    model = Availablity.time_slot.through


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here: ", db_field.name)
        if db_field.name == "doctor":
            kwargs["queryset"] = Doctor.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ["js/time-shortcuts.js"]


@admin.register(Availablity)
class Availability(admin.ModelAdmin):
    inlines = [TimeSlotInline]


admin.site.register(TimeSlot)
