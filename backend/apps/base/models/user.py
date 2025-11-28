from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        MEDICO = "medico", "Médico"
        SECRETARIA = "secretaria", "Secretaria"

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.SECRETARIA
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"