
from django.db.models import F, Value
from django.db.models.functions import Concat
from framework.permisos import P, PermisoGroup
from framework.models.basemodels import Constant

from apps.auth.models.user import User
from apps.auth.serializers.user_serializer import (
    UserUpdateSerializer,
    UserRetrieveSerializer,
    UserInputSerializer)
from controllers.base.base_rest_controller import ModelRestController, Capability, CapabilitySet
from apps.base.rest_controllers.persona_user_rest_controller import PermisosPersonaUser

class UserPermisos(PermisoGroup):
    CREATE=Constant("auth.user.create")
class UserRestController(ModelRestController):
    label = "User"
    model = User
    url = 'user'
    create_serializer = UserInputSerializer
    update_serializer = UserUpdateSerializer
    retrieve_serializer = UserRetrieveSerializer 
    permisos=[]  
    

    def create(self, request):
        return None

    def update(self, request):
        return None

    def serialize_list(self, queryset):        
        return list(queryset.values("id", "username", "is_active", "created_at"))
