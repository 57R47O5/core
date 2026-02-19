from django.db import models
from framework.models.basemodels import ConstantModel,  ConstantModelManager, Constant

class DistritoElectoralManager(ConstantModelManager):
    ASUNCION=Constant("Asuncion")
    SAN_LORENZO=Constant("San Lorenzo")
    LUQUE=Constant("Luque")

class DistritoElectoral(ConstantModel):
    '''
    Representa el donde se realiza una determinada elección
    '''
    objects=DistritoElectoralManager()

    class Meta:
        managed = False
        db_table = "distrito_electoral"

    def __str__(self):
        return self.codigo