from django import forms
from apps.profile.models import Doctor, Department, Patient
from apps.appointment.models import Appointment, AvailableTime

from django.db import transaction

from datetime import datetime


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("appointment_date", "department", "doctor")

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # self.fields["time_slot_from"].widget.attrs["class"] = "clockpicker"
        self.fields["doctor"].queryset = Doctor.objects.none()
        # self.fiekds["patient"].queryset = Patient.objects.get(user=request.user)
        if "department" in self.data:
            try:
                department_id = int(self.data.get("department"))
                self.fields["doctor"].queryset = Doctor.objects.filter(
                    department=department_id
                ).order_by("user")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        elif self.instance.pk:
            self.fields["doctor"].queryset = self.instance.department.doctor_set

        if "appointment_date" in self.data:
            self.fields["appointment_date"].input_formats = ["%B %d, %Y"]

