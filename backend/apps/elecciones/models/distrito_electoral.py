from django.db import models
from django.db.models import Value, F
from django.db.models.functions import Concat
from framework.models.basemodels import ConstantModel,  ConstantModelManager, Constant

class DistritoElectoralManager(ConstantModelManager):
    ...
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
