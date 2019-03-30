from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from apps.profile.models import Doctor, User, Patient
from apps.hospital.models import Department
from django.http import JsonResponse
import datetime
from apps.appointment.models import (
    Appointment,
    TimeSlot,
    Availablity,
    AvailableTime,
    MiddlewareNotification,
)
from django.urls import reverse_lazy
from apps.appointment.forms import AppointmentForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from notifications.signals import notify

# Create your views here.
class AppointmentDoctorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = "appointment/doctor_appointment_list.html"
    context_object_name = "appointment_list"
    login_url = "/users/login/"

    def test_func(self):
        return self.request.user.is_doctor()

    def get_queryset(self):
        doctor = Doctor.objects.get(user_id=self.request.user)
        return Appointment.objects.filter(doctor_id=doctor)


class AppointmentPatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = "appointment/patient_appointment_list.html"
    context_object_name = "appointment_list"

    def test_func(self):
        return self.request.user.is_patient()


class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = "/users/login/"
    permission_denied_message = "You have no permission to view this page."

    model = Appointment
    form_class = AppointmentForm
    template_name = "appointment/appointment_create.html"
    success_url = reverse_lazy("create-appointment")

    def test_func(self):
        return self.request.user.is_patient()

    def form_invalid(self, form):
        print(form.data)
        print(form.errors)
        messages.error(self.request, "Something went wrong.")
        return super().form_invalid(form)

    @transaction.atomic
    def form_valid(self, form):
        print("HERE: ")
        available_timeslot_id = form.data.get("available_timeslot_id")
        doctor_id = form.data.get("doctor")
        available_timeslot = AvailableTime.objects.get(pk=available_timeslot_id)
        available_timeslot.status = False
        available_timeslot.save()
        print("AVAILABLE: ", available_timeslot.timeslot)
        patient = Patient.objects.get(user=self.request.user.id)
        form.instance.patient = patient
        form.instance.timeslot = available_timeslot.timeslot
        doctor = Doctor.objects.get(user=doctor_id)
        user = User.objects.get(pk=doctor.user.id)
        notify.send(patient, recipient=user, verb="appointment created")

        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = "/users/login/"
    model = Appointment
    context_object_name = "appointment_list"
    success_url = reverse_lazy("list-doctor-appointment")
    fields = ("status",)

    def test_func(self):
        return self.request.user.is_doctor()

    @transaction.atomic
    def get_object(self):

        appointment_id = self.request.GET["appointment_id"]
        status = self.request.GET["status"]
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.status = status
        appointment.save()
        return appointment


def load_doctors(request):
    department_id = request.GET.get("department")
    doctors = Doctor.objects.filter(department_id=department_id).order_by("user")
    return render(request, "appointment/doctor_dropdown_list_options.html", {"doctors": doctors})


def load_time_slots(requests):
    date = requests.GET.get("date")
    print(requests.GET)
    pasrsed_date = datetime.datetime.strptime(date, "%B %d, %Y")
    doctor_id = requests.GET.get("doctor")
    available = Availablity.objects.get(date=pasrsed_date, doctor_id=doctor_id)
    time_slot = available.available_time.filter(status=True)
    return render(requests, "appointment/doctor_availability.html", {"time_slots": time_slot})


def notify_create(request):
    appointment_id = request.GET.get("appointment_id")
    new_notification = MiddlewareNotification(
        user=request.user, appointment=Appointment.objects.get(pk=appointment_id)
    )

    return JsonResponse({"created": "New appointment has been created."})


def load_available_date(request):
    date_object = datetime.date.today()
    try:
        availabilities = Availablity.objects.filter(date__gte=date_object).order_by("date")
    except:
        availabilities = None

    print(availabilities)

    return render(request, "appointment/available_date.html", {"availabilities": availabilities})
