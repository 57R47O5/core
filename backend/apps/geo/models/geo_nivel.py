from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class GeoNivelManager(ConstantModelManager):
    PAIS = Constant("PAIS", orden=1)
    DEPARTAMENTO = Constant("DEPARTAMENTO", orden=2)
    DISTRITO = Constant("DISTRITO", orden=3)
    BARRIO = Constant("BARRIO", orden=4)
    PUNTO = Constant("PUNTO", orden=5)

class GeoNivel(ConstantModel):
    '''
    Define el nivel en que se encuentra una entidad geográfica
    '''
    orden=models.FloatField("orden de los niveles")

    objects = GeoNivelManager()

    class Meta:
        db_table= 'geo_nivel'
        managed = False