from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.votante import Votante
from apps.elecciones.serializers.votante_serializer import (
    VotanteCreateSerializer,
    VotanteUpdateSerializer,
    VotanteRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class VotanteRestController(ModelRestController):
    model = Votante
    create_serializer = VotanteCreateSerializer
    update_serializer = VotanteUpdateSerializer
    retrieve_serializer = VotanteRetrieveSerializer    
