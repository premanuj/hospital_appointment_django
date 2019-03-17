from django.urls import path, re_path
from django.contrib.auth import views
from .views import (
    AppointmentCreateView,
    AppointmentListView,
    AppointmentUpdateView,
    load_doctors,
    load_time_slots,
)


urlpatterns = [
    path("create/", AppointmentCreateView.as_view(), name="create-appointment"),
    path(
        "update/",
        AppointmentUpdateView.as_view(template_name="appointment/appointment_create.html"),
        name="update-appointment",
    ),
    path(
        "list/",
        AppointmentListView.as_view(template_name="appointment/appointment_list/logout.html"),
        name="list-appointment",
    ),
    path("ajax/load-doctors/", load_doctors, name="ajax_load_doctors"),  # <-- this one here
    path("ajax/load-time-slots/", load_time_slots, name="ajax_load_timeslots"),  # <-- this one here
]
