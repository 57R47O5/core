from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.base.models.persona_user import PersonaUser
from apps.base.serializers.persona_user_serializer import (
    PersonaUserCreateSerializer,
    PersonaUserUpdateSerializer,
    PersonaUserRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class PersonaUserRestController(ModelRestController):
    model = PersonaUser
    url = 'persona-user'
    permisos = []
    create_serializer = PersonaUserCreateSerializer
    update_serializer = PersonaUserUpdateSerializer
    retrieve_serializer = PersonaUserRetrieveSerializer
