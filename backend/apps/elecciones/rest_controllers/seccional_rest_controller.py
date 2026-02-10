from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.seccional import Seccional
from apps.elecciones.serializers.seccional_serializer import (
    SeccionalCreateSerializer,
    SeccionalUpdateSerializer,
    SeccionalRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class SeccionalRestController(ModelRestController):
    model = Seccional
    create_serializer = SeccionalCreateSerializer
    update_serializer = SeccionalUpdateSerializer
    retrieve_serializer = SeccionalRetrieveSerializer    
