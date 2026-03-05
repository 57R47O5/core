from django.db.models import Q, F
from rest_framework import status
from rest_framework.response import Response

from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant
from framework.exceptions import excepcion, ExcepcionValidacion
from framework.api.options import BaseOptionsAPIView
from apps.auth.models.user_rol import UserRol
from apps.auth.serializers.user_rol_serializer import (
    UserRolCreateSerializer,
    UserRolUpdateSerializer,
    UserRolRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosUserRol(PermisoGroup):
    VIEW=Constant("auth.user_rol.view")
    CREATE=Constant("auth.user_rol.create")
    UPDATE=Constant("auth.user_rol.update")
    DESTROY=Constant("auth.user_rol.destroy")


class UserRolRestController(ModelRestController):
    label = "UserRol"
    model = UserRol
    url = "user-rol"
    create_serializer = UserRolCreateSerializer
    update_serializer = UserRolUpdateSerializer
    retrieve_serializer = UserRolRetrieveSerializer    
    permisos = PermisosUserRol

    def serialize_list(self, queryset):
        return queryset.values().annotate(
            nombre=F("rol__nombre"),
            descripcion=F("rol__nombre"),
            rol=F("rol_id"),
            ).values()
    
    @excepcion
    def create(self, request):
        datos=request.data.copy()
        datos_listos = {
            'user': datos.pop('id'),
            'rol': datos.pop('rol')
        }
        serializer=self.create_serializer(data=datos_listos)
        if not serializer.is_valid():
            raise ExcepcionValidacion(str(serializer.errors))
        instancia=serializer.save()
        return Response(self._serialize_instance(request, instancia), status=status.HTTP_201_CREATED)
