from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from apps.base.models.persona_juridica import PersonaJuridica
from apps.base.serializers.persona_juridica_serializer import (
    PersonaJuridicaUpdateSerializer,
    PersonaJuridicaInputSerializer,
    PersonaJuridicaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosPersonaJuridica(PermisoGroup):
    VIEW=Constant("base.persona-juridica.view")
    CREATE=Constant("base.persona-juridica.create")
    UPDATE=Constant("base.persona-juridica.update")
    DESTROY=Constant("base.persona-juridica.destroy")
class PersonaJuridicaRestController(ModelRestController):
    label="Empresas"
    model = PersonaJuridica
    url = 'persona-juridica'
    create_serializer = PersonaJuridicaInputSerializer
    update_serializer = PersonaJuridicaUpdateSerializer
    retrieve_serializer = PersonaJuridicaRetrieveSerializer
    permisos = PermisosPersonaJuridica


