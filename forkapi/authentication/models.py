from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True, max_length=100)
    is_superuser = BooleanField(default=True)
    is_staff = BooleanField(default=True)
