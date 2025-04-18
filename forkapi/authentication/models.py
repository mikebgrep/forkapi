from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField, CASCADE
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True, max_length=100)
    is_superuser = BooleanField(default=True)
    is_staff = BooleanField(default=True)


class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSettings(models.Model):
    preferred_translate_language = models.CharField(max_length=20, null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="settings")
    compact_pdf = models.BooleanField(default=False)
    # TODO:// add unit conversion choice
