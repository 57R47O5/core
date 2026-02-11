
from framework.api.options import BaseOptionsAPIView
from framework.permisos import P

from apps.base.models.persona_fisica import PersonaFisica
from apps.base.permisos import PermisosPersonaFisica
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    PersonaFisicaInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PersonaFisicaRestController(ModelRestController):
    label = "Persona"
    model = PersonaFisica
    url = 'persona-fisica'
    create_serializer = PersonaFisicaInputSerializer
    update_serializer = PersonaFisicaUpdateSerializer
    retrieve_serializer = PersonaFisicaRetrieveSerializer 

    create_permission = P(PermisosPersonaFisica.CREATE)
    update_permission = P(PermisosPersonaFisica.UPDATE)
    destroy_permission = P(PermisosPersonaFisica.DESTROY)
    view_permission = P(PermisosPersonaFisica.VIEW)
    
    permisos = create_permission and update_permission \
        and destroy_permission and view_permission
