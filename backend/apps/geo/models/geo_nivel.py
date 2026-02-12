from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class GeoNivelManager(ConstantModelManager):
    PAIS = Constant("PAIS")
    DEPARTAMENTO = Constant("DEPARTAMENTO")
    DISTRITO = Constant("DISTRITO")
    BARRIO = Constant("BARRIO")
    PUNTO = Constant("PUNTO")

class GeoNivel(ConstantModel):
    '''
    Define el nivel en que se encuentra una entidad geográfica
    '''
    objects = GeoNivelManager()

    class Meta:
        db_table= 'geo_nivel'
        managed = False