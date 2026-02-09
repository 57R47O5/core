
from framework.permisos import P

from apps.geo.models.lugar import Lugar
from apps.geo.permisos import GeoPermisos
from apps.geo.serializers.lugar_serializer import (
    LugarUpdateSerializer,
    LugarRetrieveSerializer,
    LugarInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class LugarRestController(ModelRestController):
    label = "Lugar"
    model = Lugar
    url = 'lugar'
    create_serializer = LugarInputSerializer
    update_serializer = LugarUpdateSerializer
    retrieve_serializer = LugarRetrieveSerializer 

    create_permission = P(GeoPermisos.LUGAR_CREATE)
    update_permission = P(GeoPermisos.LUGAR_UPDATE)
    destroy_permission = P(GeoPermisos.LUGAR_DESTROY)
    view_permission = P(GeoPermisos.LUGAR_VIEW)
    
    permisos = create_permission and update_permission \
        and destroy_permission and view_permission
