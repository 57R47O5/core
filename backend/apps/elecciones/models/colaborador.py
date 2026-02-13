from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.campana import Campana

class Colaborador(BaseModel):
    persona = models.ForeignKey(PersonaFisica, on_delete=models.CASCADE)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, 
        related_name='colaboradores', db_index=True)

    class Meta:
        managed=False
        db_table="colaborador"

    constraints = [
        models.UniqueConstraint(
            fields=["persona", "campana"],
            name="uq_colaborador_persona_campana")
        ]

    def __str__(self):
        return f"{str(self.persona)} - {self.campana}"