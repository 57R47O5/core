
from framework.api.options import BaseOptionsAPIView
from controllers.base.base_rest_controller import ModelRestController
from apps.auth.models.rol import Rol

class RolRestController(ModelRestController):
    model = Rol
    url='rol'
    permisos=[]

class RolOptionsView(BaseOptionsAPIView):
    model = Rol
    url='rol'
    desc_field='nombre'
    permisos=[]

