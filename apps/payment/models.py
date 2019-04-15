from django.db import models
from apps.appointment.models import Appointment
from apps.profile.models import User

# Create your models here.


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
