from apps.auth.models.permiso import PermisoManager
from framework.models.basemodels import Constant
from apps.auth.rest_controllers.user_rest_controller import UserPermisos
from apps.auth.rest_controllers.rol_permiso_rest_controller import PermisosRolPermiso  
from apps.auth.rest_controllers.user_rol_rest_controller import PermisosUserRol

class AuthPermisos(PermisoManager):

    grupos = [
        UserPermisos,
        PermisosRolPermiso,
        PermisosUserRol  
    ]