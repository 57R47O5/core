from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.visita import Visita
from apps.elecciones.serializers.visita_serializer import (
    VisitaCreateSerializer,
    VisitaUpdateSerializer,
    VisitaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosVisita(PermisoGroup):
    VIEW=Constant("elecciones.visita.view")
    CREATE=Constant("elecciones.visita.create")
    UPDATE=Constant("elecciones.visita.update")
    DESTROY=Constant("elecciones.visita.destroy")


class VisitaRestController(ModelRestController):
    label = "Visita"
    model = Visita
    url = "visita"
    create_serializer = VisitaCreateSerializer
    update_serializer = VisitaUpdateSerializer
    retrieve_serializer = VisitaRetrieveSerializer    
    permisos = PermisosVisita
