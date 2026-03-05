from django.db.models import Q, F
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.auth.models.rol_permiso import RolPermiso
from apps.auth.serializers.rol_permiso_serializer import (
    RolPermisoCreateSerializer,
    RolPermisoUpdateSerializer,
    RolPermisoRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosRolPermiso(PermisoGroup):
    VIEW=Constant("auth.rol_permiso.view")
    CREATE=Constant("auth.rol_permiso.create")
    UPDATE=Constant("auth.rol_permiso.update")
    DESTROY=Constant("auth.rol_permiso.destroy")


class RolPermisoRestController(ModelRestController):
    label = "RolPermiso"
    model = RolPermiso
    url = "rol-permiso"
    create_serializer = RolPermisoCreateSerializer
    update_serializer = RolPermisoUpdateSerializer
    retrieve_serializer = RolPermisoRetrieveSerializer    
    permisos = PermisosRolPermiso

    def serialize_list(self, queryset):
        return queryset.values().annotate(nombre=F("rol__nombre")).values()