from django import forms
from apps.profile.models import Doctor, Department
from apps.appointment.models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("appointment_date", "time_slot_from", "department", "doctor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.none()

        if "appointment" in self.data:
            try:
                appointment_id = int(self.data.get("appointment"))
                self.fields["city"].queryset = Doctor.objects.filter(
                    appointment=appointment_id
                ).order_by("user")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields["city"].queryset = self.instance.country.city_set.order_by("name")

