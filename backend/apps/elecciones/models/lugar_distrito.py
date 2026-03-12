from django.db import models
from framework.models.basemodels import BaseModel
from apps.geo.models.lugar import Punto
from apps.elecciones.models.distrito_electoral import DistritoElectoral

class LugarDistrito(BaseModel):
    '''
    Define la ubicación geográfica de un distrito
    '''
    distrito = models.ForeignKey(
        DistritoElectoral,
        on_delete=models.CASCADE,
        related_name="fronteras",
        db_column="distrito"
    )

    lugar = models.ForeignKey(
        Punto,
        on_delete=models.PROTECT,
        db_column="lugar"
    )

    class Meta:
        managed = False
        db_table = "lugar_distrito"
