from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from apps.hospital.models import Department


class User(AbstractUser):
    PATIENT = 1
    DOCTOR = 2
    ADMIN = 4
    ROLE_CHOICES = ((PATIENT, "Patient"), (DOCTOR, "Doctor"), (ADMIN, "Admin"))
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    def is_doctor(self):
        return self.role == self.DOCTOR

    def is_patient(self):
        return self.role == self.PATIENT

    class Meta:
        verbose_name_plural = "Users"


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts"
    )
    contact_no = models.IntegerField(unique=True)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    education = models.CharField(max_length=500, null=True)
    time_slot = models.DurationField()

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = "Doctors"


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = "Patients"

