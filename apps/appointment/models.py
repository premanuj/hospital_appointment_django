from django.db import models
from apps.profile.models import Doctor, Patient
from apps.hospital.models import Department
from django.conf import settings
from django.db.models.signals import post_save
from notifications.signals import notify

# Create your models here.


class TimeSlot(models.Model):
    available_from = models.TimeField(("Appointment time starts"))
    available_to = models.TimeField(("Appointment time ends"))

    def __str__(self):
        return f"Start time: {self.available_from} End time: {self.available_to}"


class Availablity(models.Model):
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot = models.ManyToManyField(TimeSlot, through="AvailableTime", related_name="available")

    def __str__(self):
        return f"Date: {self.date}"

    class Meta:
        verbose_name_plural = "availablities"


class AvailableTime(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="available_time")
    availablity = models.ForeignKey(
        Availablity, on_delete=models.CASCADE, related_name="available_time"
    )
    status = models.BooleanField(default=True)


class Appointment(models.Model):
    CONFIRMED = 1
    CANCELLED = 2
    WAITING = 3
    STATUS_CODES = ((CONFIRMED, "Confirmed"), (CANCELLED, "Cancelled"), (WAITING, "Waiting"))
    appointment_date = models.DateField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CODES, null=True, default=WAITING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True)


# def appointment_created_notification(sender, instance, *args, **kwagrs):
#     notify.send(instance, "appointment created.")
# post_save.connect(appointment_created_notification, sender=Appointment)


class MiddlewareNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        if self.user.is_doctor:
            return f"{self.user} accepts {self.appointment}"
        return f"{self.user} requests for {self.appointment}"
