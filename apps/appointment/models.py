from django.db import models
from apps.profile.models import Doctor, Patient
from apps.hospital.models import Department

# Create your models here.


# class DaySchedule(models.Model):
#     MONDAY = 1
#     TUESDAY = 2
#     WEDNESDAY = 3
#     THURSDAY = 4
#     FRIDAY = 5
#     SATURDAY = 6
#     SUNDAY = 7
#     DAYS = (
#         (MONDAY, "Monday"),
#         (TUESDAY, "Tuesday"),
#         (WEDNESDAY, "Wednesday"),
#         (THURSDAY, "Thursday"),
#         (FRIDAY, "Friday"),
#         (SATURDAY, "Saturday"),
#         (SUNDAY, "Sunday"),
#     )
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     day = models.PositiveSmallIntegerField(choices=DAYS)
#     time_slot_from = models.TimeField()
#     time_slot_to = models.TimeField()


class Appointment(models.Model):
    CONFIRMED = 1
    CANCELLED = 2
    WAITING = 3
    STATUS_CODES = ((CONFIRMED, "Confirmed"), (CANCELLED, "Cancelled"), (WAITING, "Waiting"))
    appointment_date = models.DateField()
    time_slot_from = models.TimeField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CODES, null=True, default=WAITING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)


class Notification(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    read = models.BooleanField(default=False)


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

