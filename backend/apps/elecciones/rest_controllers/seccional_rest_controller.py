from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.seccional import Seccional
from apps.elecciones.serializers.seccional_serializer import (
    SeccionalCreateSerializer,
    SeccionalUpdateSerializer,
    SeccionalRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosSeccional(PermisoGroup):
    VIEW=Constant("elecciones.seccional.view")
    CREATE=Constant("elecciones.seccional.create")
    UPDATE=Constant("elecciones.seccional.update")
    DESTROY=Constant("elecciones.seccional.destroy")


class SeccionalRestController(ModelRestController):
    label = "Seccional"
    model = Seccional
    url = "seccional"
    create_serializer = SeccionalCreateSerializer
    update_serializer = SeccionalUpdateSerializer
    retrieve_serializer = SeccionalRetrieveSerializer    
    permisos = PermisosSeccional
