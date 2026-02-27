from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant
from apps.base.models.persona_user import PersonaUser
from apps.base.serializers.persona_user_serializer import (
    PersonaUserCreateSerializer,
    PersonaUserUpdateSerializer,
    PersonaUserRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosPersonaUser(PermisoGroup):
    VIEW=Constant("base.persona_user.view")
    CREATE=Constant("base.persona_user.create")
    UPDATE=Constant("base.persona_user.update")
    DESTROY=Constant("base.persona_user.destroy")
class PersonaUserRestController(ModelRestController):
    model = PersonaUser
    url = 'persona-user'
    permisos = []
    create_serializer = PersonaUserCreateSerializer
    update_serializer = PersonaUserUpdateSerializer
    retrieve_serializer = PersonaUserRetrieveSerializer
