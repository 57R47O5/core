from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.serializers.colaborador_serializer import (
    ColaboradorCreateSerializer,
    ColaboradorUpdateSerializer,
    ColaboradorRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class ColaboradorRestController(ModelRestController):
    model = Colaborador
    create_serializer = ColaboradorCreateSerializer
    update_serializer = ColaboradorUpdateSerializer
    retrieve_serializer = ColaboradorRetrieveSerializer    
