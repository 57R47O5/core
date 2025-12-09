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

    # Datos personales
    nombres = models.CharField(max_length=40, blank=True, null=True)
    apellidos = models.CharField(max_length=40, blank=True, null=True)
    dni = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)

    # Datos profesionales
    matricula = models.CharField(max_length=30, blank=True, null=True)
    especialidad = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.username}"