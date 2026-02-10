from django.db import models
from framework.models.basemodels import BaseModel
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.campana import Campana

class Seccional(BaseModel):
    '''
    División territorial de una determinada campaña
    Su función es estratégica. Cada campaña decide 
    cómo dividir su territorio
    '''
    zona = models.ForeignKey(Lugar, on_delete=models.PROTECT, related_name='zonas')
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name="seccionales")

    class Meta:
        managed=False
        db_table="seccional"