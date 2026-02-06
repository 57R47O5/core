
from framework.api.options import BaseOptionsAPIView
from framework.permisos import P

from apps.base.models.persona_fisica import PersonaFisica
from apps.base.permisos import BasePermisos
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    PersonaFisicaInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PersonaFisicaRestController(ModelRestController):
    label = "Persona"
    model = PersonaFisica
    url = 'persona-fisica'
    permisos= None
    create_serializer = PersonaFisicaInputSerializer
    update_serializer = PersonaFisicaUpdateSerializer
    retrieve_serializer = PersonaFisicaRetrieveSerializer 

    create_permission = P(BasePermisos.PERSONA_FISICA_CREATE)
    update_permission = P(BasePermisos.PERSONA_FISICA_UPDATE)
    destroy_permission = P(BasePermisos.PERSONA_FISICA_DESTROY)
    view_permission = P(BasePermisos.PERSONA_FISICA_VIEW)
