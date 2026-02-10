from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.campana import Campana
from apps.elecciones.serializers.campana_serializer import (
    CampanaCreateSerializer,
    CampanaUpdateSerializer,
    CampanaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class CampanaRestController(ModelRestController):
    model = Campana
    create_serializer = CampanaCreateSerializer
    update_serializer = CampanaUpdateSerializer
    retrieve_serializer = CampanaRetrieveSerializer    
