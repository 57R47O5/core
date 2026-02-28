from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from framework.permisos import P, PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.serializers.colaborador_serializer import (
    ColaboradorCreateSerializer,
    ColaboradorUpdateSerializer,
    ColaboradorRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController,  Capability, CapabilitySet
from apps.base.rest_controllers.persona_user_rest_controller import PermisosPersonaUser
from apps.auth.models.user import User

class PermisosColaborador(PermisoGroup):
    VIEW=Constant("elecciones.colaborador.view")
    CREATE=Constant("elecciones.colaborador.create")
    UPDATE=Constant("elecciones.colaborador.update")
    DESTROY=Constant("elecciones.colaborador.destroy")


class ColaboradorRestController(ModelRestController):
    label = "Colaborador"
    model = Colaborador
    url = "colaborador"
    create_serializer = ColaboradorCreateSerializer
    update_serializer = ColaboradorUpdateSerializer
    retrieve_serializer = ColaboradorRetrieveSerializer    
    permisos = PermisosColaborador

    capabilities = CapabilitySet(
        Capability(
            name="crear_usuario",
            permission=P(PermisosPersonaUser.CREATE),
            business_rule=lambda instancia: instancia.usuario_agregable
        )
    )

    def serialize_list(self, queryset):
        return list(queryset.values()
                    .annotate(
                        nombres=F("persona__nombres"),
                        apellidos=F("persona__apellidos"),
                    ).annotate(
                        descripcion=Concat(
                        F("nombres"),
                        Value(" "),
                        F("apellidos"),
                        )
                    ).values())
    
    def _get_filter(self, params):
        filtro = Q()
        for key, value in params.items():
            if key in  ['nombres', 'apellidos']:
                filtro &= Q(**{f"persona__{key}__icontains":value})
        return filtro
    
    #Por ahora está bien así
    @action(methods=["get"], detail=False, url_path="usuarios-disponibles", url_name="usuarios-disponibles")
    def get_usuarios_disponibles(self, request):
        usuarios_sin_colaboradores = User.objects.filter(personas__persona__isnull=True)
        salida= usuarios_sin_colaboradores.values("id", "username")
        return Response(salida, status=status.HTTP_200_OK)
