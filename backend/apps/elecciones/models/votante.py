from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona_fisica import PersonaFisica
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.seccional import Seccional

class Votante(BaseModel):
    persona = models.OneToOneField(PersonaFisica, on_delete=models.PROTECT)
    distrito = models.ForeignKey(Lugar, on_delete=models.PROTECT, 
        verbose_name="división territorial del votante")
    seccional = models.ForeignKey(Seccional, on_delete=models.PROTECT,
        verbose_name="división territorial de la campaña", db_index=False, 
        blank=True, null=True)

    class Meta:
        managed = False
        db_table = "votante"
