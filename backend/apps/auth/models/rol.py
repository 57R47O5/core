from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ConstantModelManager

class RolManager(ConstantModelManager):
    OWNER = Constant("owner")

class Rol(ConstantModel):
    """
    Rol del sistema.
    Agrupa permisos.
    No contiene lógica de autorización.
    """
    objects=RolManager()
    
    class Meta:
        db_table = "rol"
        managed=False
        verbose_name = "Rol"
        verbose_name_plural = "Roles"