from framework.models.basemodels import Constant
from auth.models.rol import RolManager
from base.permisos import (
    PermisosPersonaFisica,
    PermisosPersonaJuridica,
    PermisosPersonaUser,
    PermisosContacto
)

class BaseRoles(RolManager):    
    BASE_VIEWER = Constant(
        "base.viewer",
        permisos=[
            PermisosPersonaFisica.VIEW,
            PermisosPersonaJuridica.VIEW,
            PermisosContacto.VIEW
        ]
    )

    BASE_ADMIN = Constant(
        "base.admin",
        permisos=[
            PermisosPersonaFisica.VIEW,
            PermisosPersonaJuridica.VIEW,
            PermisosPersonaJuridica.UPDATE,
            PermisosPersonaUser.all(),
            PermisosContacto.all()
        ]
    )