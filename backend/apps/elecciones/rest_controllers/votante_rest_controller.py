from django.db.models import Q, F
from framework.permisos import PermisoGroup
from framework.models.basemodels import Constant

from framework.api.options import BaseOptionsAPIView
from apps.elecciones.models.votante import Votante
from apps.elecciones.serializers.votante_serializer import (
    VotanteCreateSerializer,
    VotanteUpdateSerializer,
    VotanteRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController

class PermisosVotante(PermisoGroup):
    VIEW=Constant("elecciones.votante.view")
    CREATE=Constant("elecciones.votante.create")
    UPDATE=Constant("elecciones.votante.update")
    DESTROY=Constant("elecciones.votante.destroy")


class VotanteRestController(ModelRestController):
    label = "Votante"
    model = Votante
    url = "votante"
    create_serializer = VotanteCreateSerializer
    update_serializer = VotanteUpdateSerializer
    retrieve_serializer = VotanteRetrieveSerializer    
    permisos = PermisosVotante

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values()
                    .annotate(
                        nombres=F("persona__nombres"),
                        apellidos=F("persona__apellidos"),
                    ).values())