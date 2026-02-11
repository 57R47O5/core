from apps.auth.models.permiso import PermisoManager
from framework.models.basemodels import Constant

class AuthPermisos(PermisoManager):
    REGISTER=Constant("auth.register")