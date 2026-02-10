from apps.auth.models.rol import RolManager
from framework.models.basemodels import Constant
from elecciones.permisos import (
        PermisosColaborador,
        PermisosCampana,
        PermisosSalida,
        PermisosSeccional,
        PermisosVisita,
        PermisosVotante)

class EleccionesRoles(RolManager):
    '''
    Estos son todos los roles que se utilizan para elecciones
    '''
    COLABORADOR=Constant(
        "elecciones.colaborador",
        permisos=[
            PermisosVisita.all(),
            PermisosSalida.all(),
            PermisosVotante.CREATE
        ])
    JEFE_CAMPANA=Constant(
        "elecciones.jefe de campaña",
        permisos=[
            PermisosColaborador.all(),
            PermisosCampana.all(),
            PermisosSalida.all(),
            PermisosSeccional.all(),
            PermisosVisita.all(),
            PermisosVotante.all()
        ]
        )
