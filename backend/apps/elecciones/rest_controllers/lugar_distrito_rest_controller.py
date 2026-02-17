from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.lugar_distrito import LugarDistrito
from apps.elecciones.serializers.lugar_distrito_serializer import (
    LugarDistritoCreateSerializer,
    LugarDistritoUpdateSerializer,
    LugarDistritoRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosLugarDistrito(PermisoGroup):
    VIEW=Constant("elecciones.lugar_distrito.view")
    CREATE=Constant("elecciones.lugar_distrito.create")
    UPDATE=Constant("elecciones.lugar_distrito.update")
    DESTROY=Constant("elecciones.lugar_distrito.destroy")


class LugarDistritoRestController(ModelRestController):
    label = "LugarDistrito"
    model = LugarDistrito
    url = "lugar-distrito"
    create_serializer = LugarDistritoCreateSerializer
    update_serializer = LugarDistritoUpdateSerializer
    retrieve_serializer = LugarDistritoRetrieveSerializer    
    permisos = PermisosLugarDistrito
