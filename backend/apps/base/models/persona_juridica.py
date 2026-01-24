from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona import Persona

class PersonaJuridica(BaseModel):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name="juridica",
    )

    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "persona_juridica"
        managed = False

    @property
    def nombre_completo(self):
        return self.nombre_fantasia or self.razon_social
