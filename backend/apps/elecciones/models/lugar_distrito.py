from django.db import models
from framework.models.basemodels import BaseModel
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.distrito_electoral import DistritoElectoral

class LugarDistrito(BaseModel):
    '''
    Define la ubicación geográfica de un distrito
    '''
    distrito = models.ForeignKey(
        DistritoElectoral,
        on_delete=models.CASCADE,
        related_name="fronteras"
    )

    lugar = models.ForeignKey(
        Lugar,
        on_delete=models.PROTECT
    )

    class Meta:
        managed = False
        db_column = "lugar_distrito"
