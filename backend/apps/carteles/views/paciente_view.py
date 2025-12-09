from django.db.models import Q
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.base.framework.api.options import BaseOptionsAPIView
from apps.carteles.models.paciente import Paciente
from apps.carteles.serializers.paciente_serializer import PacienteSerializer


@api_view(['GET', 'POST'])
def paciente_list_create(request):
    """
    GET: Listar todos los pacientes
    POST: Crear un nuevo paciente
    """
    if request.method == 'GET':
        pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def paciente_detail(request, pk):
    """
    GET: Obtener un paciente
    PUT: Actualizar un paciente
    DELETE: Eliminar un paciente
    """
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'GET':
        serializer = PacienteSerializer(paciente)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PacienteSerializer(paciente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        paciente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def paciente_search(request):
    """
    Endpoint de búsqueda avanzada de pacientes.
    Permite filtrar por: nombre, apellido, dni, fecha_desde, fecha_hasta.
    GET /api/pacientes/buscar/?nombre=Juan&apellido=Perez&dni=1234
    """
    
    params = request.GET  # QueryDict

    filtros = Q()

    # --- Campos simples ---
    nombre = params.get("nombre")
    apellido = params.get("apellido")
    dni = params.get("dni")

    if nombre:
        filtros &= Q(nombre__icontains=nombre.strip())

    if apellido:
        filtros &= Q(apellido__icontains=apellido.strip())

    if dni:
        filtros &= Q(dni__icontains=dni.strip())

    # --- Rangos de fecha (usamos fecha_creacion por ahora) ---
    fecha_desde = params.get("fecha_desde")
    fecha_hasta = params.get("fecha_hasta")

    if fecha_desde:
        try:
            fecha = datetime.fromisoformat(fecha_desde)
            filtros &= Q(fecha_creacion__date__gte=fecha.date())
        except:
            pass  # evitamos romper la búsqueda

    if fecha_hasta:
        try:
            fecha = datetime.fromisoformat(fecha_hasta)
            filtros &= Q(fecha_creacion__date__lte=fecha.date())
        except:
            pass

    pacientes = (
        Paciente.objects
        .filter(filtros)
        .order_by("apellido", "nombre")[:50]
    )

    serializer = PacienteSerializer(pacientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class PacienteNombreOptions(BaseOptionsAPIView):
    model=Paciente
    field=['nombre', 'apellido', 'dni']