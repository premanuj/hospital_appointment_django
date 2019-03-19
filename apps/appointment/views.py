from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from apps.profile.models import Doctor
from apps.hospital.models import Department
from apps.appointment.models import Appointment, TimeSlot, Availablity
from django.urls import reverse_lazy
from apps.appointment.forms import AppointmentForm
from django.contrib import messages

# Create your views here.
class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointment/appointment_list.html"
    context_object_name = "appointment_list"


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment/appointment_create.html"
    success_url = reverse_lazy("create-appointment")

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong.")
        return super().form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        Appointment.objects.create(**data)
        return super().form_valid(form)


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment/appointment_update.html"
    success_url = reverse_lazy("update-appointment")
    # fields = ("appointment_date", "time_slot_from", "doctor")


def load_doctors(request):
    department_id = request.GET.get("department")
    doctors = Doctor.objects.filter(department_id=department_id).order_by("user")
    return render(request, "appointment/doctor_dropdown_list_options.html", {"doctors": doctors})


def load_time_slots(requests):
    date = requests.GET.get("date")
    doctor_id = requests.GET.get("doctor")
    time_slots = TimeSlot.objects.filter(
        available_time__availablity__doctor=doctor_id,
        available_time__availablity__date=date,
        available_time__status=True,
    )

    return render(requests, "appointment/doctor_availability.html", {"time_slots": time_slots})
