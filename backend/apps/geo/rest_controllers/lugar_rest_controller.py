
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from apps.geo.models.lugar import Lugar
from apps.geo.serializers.lugar_serializer import (
    LugarUpdateSerializer,
    LugarRetrieveSerializer,
    LugarInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosLugar(PermisoGroup):
    VIEW=Constant("geo.lugar.view")
    CREATE=Constant("geo.lugar.create")
    UPDATE=Constant("geo.lugar.update")
    DESTROY=Constant("geo.lugar.destroy")

class LugarRestController(ModelRestController):
    label = "Lugar"
    model = Lugar
    url = 'lugar'
    create_serializer = LugarInputSerializer
    update_serializer = LugarUpdateSerializer
    retrieve_serializer = LugarRetrieveSerializer 
    
    permisos = PermisosLugar
