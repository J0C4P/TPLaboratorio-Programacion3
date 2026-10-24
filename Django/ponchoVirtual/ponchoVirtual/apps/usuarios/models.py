from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    documento_identidad = models.CharField(max_length=8, unique=True)

    REQUIRED_FIELDS = ['email', 'documento_identidad']

    def str(self):
        return f"{self.username} dni: {self.documento_identidad}"
