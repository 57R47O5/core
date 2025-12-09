from django.db.models import Q
from datetime import datetime

from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.models.paciente import Paciente
from apps.carteles.serializers.paciente_serializer import PacienteSerializer
from controllers.base.base_rest_controller import ModelRestController


class PacienteRestController(ModelRestController):
    model=Paciente
    create_serializer=PacienteSerializer
    update_serializer=PacienteSerializer
    retrieve_serializer=PacienteSerializer

    def _get_filter(self, params):
        filtros = Q()

        nombre = params.get("nombre")
        apellido = params.get("apellido")
        dni = params.get("dni")

        if nombre:
            filtros &= Q(nombre__icontains=nombre.strip())

        if apellido:
            filtros &= Q(apellido__icontains=apellido.strip())

        if dni:
            filtros &= Q(dni__icontains=dni.strip())

        # --- filtros por rango de fecha ---
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
        return self.model.objects.filter(filtro)\
            .order_by('apellido', 'nombre')

class PacienteNombreOptions(BaseOptionsAPIView):
    model=Paciente
    field=['nombre', 'apellido', 'dni']