from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona_fisica import PersonaFisica
from apps.geo.models.lugar import Lugar

from apps.elecciones.models.ciclo_electoral import CicloElectoral


class Campana(BaseModel):
    """
    Campaña: candidato + distrito + ciclo (año/elección)
    """
    candidato = models.ForeignKey(PersonaFisica, on_delete=models.PROTECT, related_name='campaigns')
    cargo = models.CharField(max_length=50)
    distrito = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='campaigns')
    ciclo = models.ForeignKey(CicloElectoral, on_delete=models.PROTECT, related_name='campaigns')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        managed=False
        db_table="campana"

    constraints = [
        models.UniqueConstraint(
            fields=["candidato", "distrito", "ciclo"],
            name="uq_campana_candidato_distrito_ciclo"
        )
    ]

    def __str__(self):
        return f"{str(self.candidato)} ({self.ciclo})"
