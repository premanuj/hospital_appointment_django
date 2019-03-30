from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from apps.hospital.models import Department


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError("Users must have username")

        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    PATIENT = 1
    DOCTOR = 2
    ADMIN = 4
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    ROLE_CHOICES = ((PATIENT, "Patient"), (DOCTOR, "Doctor"), (ADMIN, "Admin"))
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    USERNAME_FIELD = "username"
    EMIAL_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name", "role", "gender", "date_of_birth", "email"]

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

    def is_doctor(self):
        return self.role == self.DOCTOR

    def is_patient(self):
        return self.role == self.PATIENT

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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

