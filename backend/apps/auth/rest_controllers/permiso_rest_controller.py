from controllers.base.base_rest_controller import ModelRestController
from apps.auth.models.permiso import Permiso

class PermisoRestController(ModelRestController):
    model = Permiso
    url='permiso'
    desc_field='Descripcion'
    permisos=[]