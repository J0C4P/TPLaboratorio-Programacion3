from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    documento_identidad = models.CharField(max_length=8, unique=True)

    def str(self):
        return f"{self.username} dni: {self.documento_identidad}"
