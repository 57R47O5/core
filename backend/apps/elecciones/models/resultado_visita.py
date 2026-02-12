from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class ResultadoVisitaManager(ConstantModelManager):
    RECHAZO=Constant("Rechazo")
    NEUTRO=Constant("Regular")
    INTERES=Constant("Interés")
    PROMESA_VOTO=Constant("Promesa de Voto")

class ResultadoVisita(ConstantModel):
    """
    Resultado estandarizado de una visita
    """

    objects = ResultadoVisitaManager()

    class Meta:
        db_table = "resultado_visita"
        managed = False