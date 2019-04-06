from django.urls import path, re_path
from .views import (
    AppointmentCreateView,
    AppointmentDoctorListView,
    AppointmentPatientListView,
    AppointmentUpdateView,
    AppointmentView,
    AvailabilityCreateView,
    AvailabilityListView,
    load_doctors,
    load_time_slots,
    load_available_date,
    doctor_response_notification,
    patient_response_notification,
)


urlpatterns = [
    path("", AppointmentView.as_view(), name="appointment"),
    path("create-appointment/", AppointmentCreateView.as_view(), name="create-appointment"),
    path("create-availability/", AvailabilityCreateView.as_view(), name="create-availability"),
    path("list-availability/", AvailabilityListView.as_view(), name="list-availability"),
    path("update/<int:id>/", AppointmentUpdateView.as_view(), name="update-appointment"),
    path("update/", AppointmentUpdateView.as_view(), name="update-appointment"),
    path("doctor-list/<str:value>", AppointmentDoctorListView.as_view(), name="list-appointment"),
    path("patient-list/", AppointmentPatientListView.as_view(), name="list-patient-appointment"),
    path("ajax/load-doctors/", load_doctors, name="ajax_load_doctors"),  # <-- this one here
    path(
        "read-notification/doctor/",
        doctor_response_notification,
        name="doctor-response-notification",
    ),
    path(
        "read-notification/patient/",
        patient_response_notification,
        name="patient-response-notification",
    ),
    path("ajax/load-time-slots/", load_time_slots, name="ajax_load_timeslots"),  # <-- this one here
    path("ajax/load-available-date/", load_available_date, name="ajax_load_available_date"),
]
