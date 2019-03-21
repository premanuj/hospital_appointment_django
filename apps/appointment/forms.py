from django import forms
from apps.profile.models import Doctor, Department
from apps.appointment.models import Appointment, AvailableTime

from django.db import transaction


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("appointment_date", "department", "doctor")

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # self.fields["time_slot_from"].widget.attrs["class"] = "clockpicker"
        print("FIELDS: ", self.fields)

        self.fields["doctor"].queryset = Doctor.objects.none()
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

    # @transaction.atomic
    # def save(self, commit=True):
    #     available_timeslot_id = self.data.get("available_timeslot_id")
    #     available_timeslot = AvailableTime.objects.get(pk=available_timeslot_id)
    #     available_timeslot.status = False
    #     available_timeslot.save()
    #     return available_timeslot

