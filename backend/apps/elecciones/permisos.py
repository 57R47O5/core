from apps.auth.models.permiso import PermisoManager
from apps.elecciones.rest_controllers.colaborador_rest_controller import PermisosColaborador
from apps.elecciones.rest_controllers.campana_rest_controller import PermisosCampana
from apps.elecciones.rest_controllers.salida_rest_controller import PermisosSalida
from apps.elecciones.rest_controllers.seccional_rest_controller import PermisosSeccional
from apps.elecciones.rest_controllers.votante_rest_controller import PermisosVotante
from apps.elecciones.rest_controllers.visita_rest_controller import PermisosVisita


class EleccionesPermisos(PermisoManager):
    '''
    Estos son todos los permisos que se utilizan para elecciones
    '''
    grupos = [
        PermisosColaborador,
        PermisosCampana,
        PermisosSalida,
        PermisosSeccional,
        PermisosVisita,
        PermisosVotante
    ] 
    
