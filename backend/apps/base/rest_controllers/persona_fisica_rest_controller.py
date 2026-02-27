
from django.db.models import F, Value
from django.db.models.functions import Concat
from framework.permisos import P, PermisoGroup
from framework.models.basemodels import Constant

from apps.base.models.persona_fisica import PersonaFisica
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    PersonaFisicaInputSerializer)
from controllers.base.base_rest_controller import ModelRestController, Capability, CapabilitySet
from apps.base.rest_controllers.persona_user_rest_controller import PermisosPersonaUser

class PermisosPersonaFisica(PermisoGroup):
    VIEW=Constant("base.persona-fisica.view")
    CREATE=Constant("base.persona-fisica.create")
    UPDATE=Constant("base.persona-fisica.update")
    DESTROY=Constant("base.persona-fisica.destroy")

class PersonaFisicaRestController(ModelRestController):
    label = "Persona"
    model = PersonaFisica
    url = 'persona-fisica'
    create_serializer = PersonaFisicaInputSerializer
    update_serializer = PersonaFisicaUpdateSerializer
    retrieve_serializer = PersonaFisicaRetrieveSerializer 
    permisos=PermisosPersonaFisica
   
    capabilities = CapabilitySet(
        Capability(
            name="crear_usuario",
            permission=P(PermisosPersonaUser.CREATE),
            business_rule=lambda instancia: instancia.usuario_agregable
        )
    )

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values()
                    .annotate(descripcion=Concat(
                        F("nombres"),
                        Value(" "),
                        F("apellidos"),
                        )))
