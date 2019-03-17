from django.db import models
from django.conf import settings

# Create your models here.


class Department(models.Model):
    department_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.department_name
