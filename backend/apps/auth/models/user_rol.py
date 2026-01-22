from django.db import models
from framework.models.basemodels import BaseModel, SAFEDELETE_PROTECT
from .user import User
from .rol import Rol

class UserRol(BaseModel):
    user = models.ForeignKey(User, on_delete=SAFEDELETE_PROTECT, related_name='roles')
    rol = models.ForeignKey(Rol, on_delete=SAFEDELETE_PROTECT)

    class Meta:
        unique_together = ('user', 'rol')
        db_table = 'user_rol'
        managed = False
        
