import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def gen_confirmation_code():
    return random.randrange(100000, 999999)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    is_agent = models.BooleanField(_("is agent"), default=False)
    is_customer = models.BooleanField(_("is customer"), default=False)
    is_confirmed = models.BooleanField(_("is confirmed"), default=False)
    confirmation_code = models.IntegerField(
        _("confirmation code"), default=gen_confirmation_code
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def image_url(self):
        return f"https://avatars.dicebear.com/api/initials/{self.first_name}+{self.last_name}.svg"


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )
    agent_display_name = models.CharField(
        _("agent display name"), max_length=150, blank=False, null=False, unique=True
    )
