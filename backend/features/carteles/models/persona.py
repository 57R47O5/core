from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    """Representa a una persona física o jurídica que puede administrar carteles."""
    class Tipo(Enum):
        FISICA = 'F'
        JURIDICA = 'J'

        @classmethod
        def choices(cls):
            return [(tipo.value, tipo.name) for tipo in cls]

    tipo = models.CharField(max_length=1, choices=Tipo.choices())
    nombre = models.CharField(max_length=255)
    documento = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nombre