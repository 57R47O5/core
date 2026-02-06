from framework.models.basemodels import Constant
from auth.models.rol import RolManager
from base.permisos import BasePermisos

#TODO: Asegurarnos de que esto funciona
class BaseRoles(RolManager):    
    BASE_VIEWER = Constant(
        "base.viewer",
        permisos=[
            BasePermisos.PERSONA_FISICA_VIEW,
            BasePermisos.PERSONA_JURIDICA_VIEW,
        ]
    )

    BASE_ADMIN = Constant(
        "base.admin",
        permisos=[
            BasePermisos.PERSONA_FISICA_VIEW,
            BasePermisos.PERSONA_JURIDICA_VIEW,
            BasePermisos.PERSONA_FISICA_EDIT,
        ]
    )