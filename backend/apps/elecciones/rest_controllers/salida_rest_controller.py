from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.salida import Salida
from apps.elecciones.serializers.salida_serializer import (
    SalidaCreateSerializer,
    SalidaUpdateSerializer,
    SalidaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class SalidaRestController(ModelRestController):
    model = Salida
    create_serializer = SalidaCreateSerializer
    update_serializer = SalidaUpdateSerializer
    retrieve_serializer = SalidaRetrieveSerializer    
