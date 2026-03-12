from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.email

    import random
    import string

    def generate_code(length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))


