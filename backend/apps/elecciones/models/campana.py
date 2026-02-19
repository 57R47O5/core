from django.db import models
from framework.models.basemodels import BaseModel
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.distrito_electoral import DistritoElectoral
from apps.elecciones.models.ciclo_electoral import CicloElectoral


class Campana(BaseModel):
    """
    Campaña: candidato + distrito + ciclo (año/elección)
    """
    candidato = models.ForeignKey(PersonaFisica, 
        on_delete=models.PROTECT, db_column="candidato",
        related_name='campaigns')
    cargo = models.CharField(max_length=50)
    distrito = models.ForeignKey(DistritoElectoral, db_column="distrito",
        on_delete=models.PROTECT, related_name='campaigns')
    ciclo = models.ForeignKey(CicloElectoral, db_column="ciclo",
        on_delete=models.PROTECT, related_name='campaigns')
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

    def create(self, candidato:PersonaFisica, **data):
        self.candidato=candidato
        return super().objects.create(**data)