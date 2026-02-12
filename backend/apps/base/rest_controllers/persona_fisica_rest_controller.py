
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from apps.base.models.persona_fisica import PersonaFisica
from apps.base.permisos import PermisosPersonaFisica
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    PersonaFisicaInputSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosPersonaFisica(PermisoGroup):
    VIEW=Constant("base.persona_fisica.view")
    CREATE=Constant("base.persona_fisica.create")
    UPDATE=Constant("base.persona_fisica.update")
    DESTROY=Constant("base.persona_fisica.destroy")
class PersonaFisicaRestController(ModelRestController):
    label = "Persona"
    model = PersonaFisica
    url = 'persona-fisica'
    create_serializer = PersonaFisicaInputSerializer
    update_serializer = PersonaFisicaUpdateSerializer
    retrieve_serializer = PersonaFisicaRetrieveSerializer 
    permisos=PermisosPersonaFisica
