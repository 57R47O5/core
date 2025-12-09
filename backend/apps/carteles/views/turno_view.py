from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
import calendar

from datetime import datetime, timedelta

from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.models.turno import Turno
from apps.carteles.serializers.turno_serializer import TurnoSerializer, TurnoListSerializer, TurnoCreateSerializer


# -------------------------------
# ESTADOS DEL TURNO (para selects)
# -------------------------------
class TurnoEstadosOptions(BaseOptionsAPIView):
    model=Turno
    field='estado'

@api_view(["GET"])
def turnos(request):
    """
    Lista turnos diarios, semanales o mensuales.
    Permite filtrar por odontólogo y paciente.
    Query params:
        - tipo: diario | semanal | mensual (default: diario)
        - fecha_inicio: YYYY-MM-DD (obligatorio)
        - odontologo: ID (opcional)
        - paciente: ID (opcional)
    """

    tipo = request.GET.get("tipo", "diario")
    fecha_str = request.GET.get("fecha_inicio")
    odontologo_id = request.GET.get("odontologo")
    paciente_id = request.GET.get("paciente")

    if not fecha_str:
        return Response(
            {"error": "Debe enviar 'fecha' en formato YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # VALIDAR FECHA
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Formato de fecha inválido"}, status=400)

    # -----------------------------
    # RANGO DE FECHAS
    # -----------------------------
    if tipo == "diario":
        desde = fecha
        hasta = fecha

    elif tipo == "semanal":
        desde = fecha
        hasta = fecha + timedelta(days=6)

    elif tipo == "mensual":
        desde = fecha.replace(day=1)
        ultimo_dia = calendar.monthrange(fecha.year, fecha.month)[1]
        hasta = fecha.replace(day=ultimo_dia)

    else:
        return Response(
            {"error": "Tipo inválido. Valores aceptados: diario, semanal, mensual"},
            status=400
        )

    # -----------------------------
    # QUERYSET
    # -----------------------------
    queryset = (
        Turno.objects
        .select_related("paciente", "odontologo") 
        .filter(fecha_inicio__range=[desde, hasta])
    )

    if odontologo_id:
        queryset = queryset.filter(odontologo_id=odontologo_id)

    if paciente_id:
        queryset = queryset.filter(paciente_id=paciente_id)

    # -----------------------------
    # SERIALIZACIÓN
    # -----------------------------
    serializer = TurnoListSerializer(queryset, many=True)
    return Response(serializer.data)


# -------------------------------
# CREAR TURNO
# -------------------------------
@api_view(["POST"])
def turno_create(request):
    serializer = TurnoCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# DETALLE / UPDATE / DELETE
# -------------------------------
@api_view(["GET", "PUT", "DELETE"])
def turno_detail(request, pk):
    try:
        turno = Turno.objects.get(pk=pk)
    except Turno.DoesNotExist:
        return Response({"error": "Turno no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Obtener turno
    if request.method == "GET":
        serializer = TurnoSerializer(turno)
        return Response(serializer.data)

    # Editar turno
    if request.method == "PUT":
        serializer = TurnoSerializer(turno, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar turno
    if request.method == "DELETE":
        turno.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
