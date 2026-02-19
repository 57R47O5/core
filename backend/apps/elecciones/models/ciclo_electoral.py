from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class CicloElectoralManager(ConstantModelManager):
    MUNICIPAL2026 = Constant("Municipales 2026")

class CicloElectoral(ConstantModel):
    '''
    Define cuando se vota
    '''
    objects = CicloElectoralManager()

    class Meta:
        db_table= 'ciclo_electoral'
        managed = False

    def __str__(self):
        return self.codigo