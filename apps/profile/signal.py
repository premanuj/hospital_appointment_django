from notifications.signals import notify
from django.db.models.signals import post_save
from apps.appointment.models import Appointment
from .models import User


def appointment_handler(sender, instance, created, **kwrgs):
    notify.send(instance, verb="was created")


post_save.connect(appointment_handler, sender=User)
