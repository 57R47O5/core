from django.db.models import Q
from datetime import datetime

from framework.api.options import BaseOptionsAPIView
from apps.base.models.moneda import Moneda
from apps.base.serializers.moneda_serializer import (
    MonedaCreateSerializer,
    MonedaUpdateSerializer,
    MonedaRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController


class MonedaRestController(ModelRestController):
    model = Moneda
    create_serializer = MonedaCreateSerializer
    update_serializer = MonedaUpdateSerializer
    retrieve_serializer = MonedaRetrieveSerializer

    def _get_filter(self, params):
        filtros = Q()

        # --- filtros automáticos por coincidencia de campos ---
        for campo, valor in params.items():
            if valor:
                filtros &= Q(**{
                    f"{campo}__icontains": valor.strip()
                })

        # --- filtros especiales (fecha_desde / fecha_hasta) ---
        fecha_desde = params.get("fecha_desde")
        fecha_hasta = params.get("fecha_hasta")

        if fecha_desde:
            try:
                fecha = datetime.fromisoformat(fecha_desde)
                filtros &= Q(fecha_creacion__date__gte=fecha.date())
            except:
                pass

        if fecha_hasta:
            try:
                fecha = datetime.fromisoformat(fecha_hasta)
                filtros &= Q(fecha_creacion__date__lte=fecha.date())
            except:
                pass

        return filtros

    def _get_queryset(self, filtro):
        return self.model.objects.filter(filtro).order_by('id')
