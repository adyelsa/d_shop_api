import random
from django.contrib.auth.models import User
from django.db import models


def generate_code():
    return str(random.randint(100000, 999999))


class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_code)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.code}"