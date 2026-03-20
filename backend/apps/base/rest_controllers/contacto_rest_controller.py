from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.base.models.contacto import Contacto
from apps.base.serializers.contacto_serializer import (
    ContactoCreateSerializer,
    ContactoUpdateSerializer,
    ContactoRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosContacto(PermisoGroup):
    VIEW=Constant("base.contacto.view")
    CREATE=Constant("base.contacto.create")
    UPDATE=Constant("base.contacto.update")
    DESTROY=Constant("base.contacto.destroy")


class ContactoRestController(ModelRestController):
    label = "Contacto"
    model = Contacto
    url = "contacto"
    create_serializer = ContactoCreateSerializer
    update_serializer = ContactoUpdateSerializer
    retrieve_serializer = ContactoRetrieveSerializer    
    permisos = PermisosContacto
