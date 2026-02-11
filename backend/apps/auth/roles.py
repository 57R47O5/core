from framework.models.basemodels import Constant
from auth.models.rol import RolManager
from auth.permisos import AuthPermisos

class AuthRoles(RolManager):    
    OWNER = Constant("owner")
    ADMIN = Constant("admin", permisos=[
        AuthPermisos.REGISTER
    ])