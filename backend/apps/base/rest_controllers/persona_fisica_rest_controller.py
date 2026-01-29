
from framework.api.options import BaseOptionsAPIView

from apps.base.models.persona_fisica import PersonaFisica
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    PersonaFisicaInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PersonaFisicaRestController(ModelRestController):
    model = PersonaFisica
    create_serializer = PersonaFisicaInputSerializer
    update_serializer = PersonaFisicaUpdateSerializer
    retrieve_serializer = PersonaFisicaRetrieveSerializer    
