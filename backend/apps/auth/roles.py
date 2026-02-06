from framework.models.basemodels import Constant
from auth.models.rol import RolManager

class AuthRoles(RolManager):    
    OWNER = Constant("owner")