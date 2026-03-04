
from controllers.base.base_rest_controller import ModelRestController
from apps.auth.models.rol import Rol

class RolRestController(ModelRestController):
    model = Rol
    url='rol'
    desc_field='Descripcion'
    permisos=[]

