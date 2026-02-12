from django.db.models import Q
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.campana import Campana
from apps.elecciones.serializers.campana_serializer import (
    CampanaCreateSerializer,
    CampanaUpdateSerializer,
    CampanaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosCampana(PermisoGroup):
    VIEW=Constant("elecciones.campana.view")
    CREATE=Constant("elecciones.campana.create")
    UPDATE=Constant("elecciones.campana.update")
    DESTROY=Constant("elecciones.campana.destroy")


class CampanaRestController(ModelRestController):
    label = "Campana"
    model = Campana
    url = "campana"
    create_serializer = CampanaCreateSerializer
    update_serializer = CampanaUpdateSerializer
    retrieve_serializer = CampanaRetrieveSerializer    
    permisos = PermisosCampana
