from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField


class User(AbstractUser):
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    is_superuser = BooleanField(default=True)
    is_staff = BooleanField(default=True)