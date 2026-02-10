from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class ResultadoVisitaManager(ConstantModelManager):
    RECHAZO=Constant("Rechazo", valor=1)
    NEUTRO=Constant("Regular", valor=2)
    INTERES=Constant("Interés", valor=3)
    PROMESA_VOTO=Constant("Promesa de Voto", valor=4)

class ResultadoVisita(ConstantModel):
    """
    Resultado estandarizado de una visita
    """
    valor=models.SmallIntegerField('Utilizamos para calcular el resultado de un conjunto de visitas')

    objects = ResultadoVisitaManager()

    class Meta:
        db_table = "resultado_visita"
        managed = False