from django.db import models
from auth.models.user import User
from framework.models.basemodels import BaseModel

class Persona(BaseModel):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="personas",
    )

    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)

    dni = models.CharField(max_length=20, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "persona"
