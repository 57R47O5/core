from apps.auth.models.permiso import PermisoManager
from apps.base.rest_controllers.persona_fisica_rest_controller import PermisosPersonaFisica
from apps.base.rest_controllers.persona_juridica_rest_controller import PermisosPersonaJuridica
from apps.base.rest_controllers.documento_identidad_rest_controller import PermisosDocumentoIdentidad

class BasePermisos(PermisoManager):
    '''
    Estos son todos los  permisos de la app base
    '''
    grupos = [
        PermisosPersonaFisica,
        PermisosPersonaJuridica,
        PermisosDocumentoIdentidad,
    ]