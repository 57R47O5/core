from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.salida import Salida
from apps.elecciones.serializers.salida_serializer import (
    SalidaCreateSerializer,
    SalidaUpdateSerializer,
    SalidaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosSalida(PermisoGroup):
    VIEW=Constant("elecciones.salida.view")
    CREATE=Constant("elecciones.salida.create")
    UPDATE=Constant("elecciones.salida.update")
    DESTROY=Constant("elecciones.salida.destroy")
    ESTADO_SALIDA_VIEW=Constant("elecciones.estado_salida.view")

class SalidaRestController(ModelRestController):
    label = "Salida"
    model = Salida
    url = "salida"
    create_serializer = SalidaCreateSerializer
    update_serializer = SalidaUpdateSerializer
    retrieve_serializer = SalidaRetrieveSerializer    
    permisos = PermisosSalida
