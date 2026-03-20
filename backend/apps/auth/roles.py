from framework.models.basemodels import Constant
from auth.models.rol import RolManager
from auth.permisos import UserPermisos, PermisosUserRol, PermisosRolPermiso

class AuthRoles(RolManager):    
    OWNER = Constant("owner")
    ADMIN = Constant("admin", permisos=[
        UserPermisos.all(),
        PermisosUserRol.all(),
        PermisosRolPermiso.all()
    ])