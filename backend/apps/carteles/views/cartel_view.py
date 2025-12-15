from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from apps.base.framework.exceptions import excepcion
from ..models.imagencartel import Cartel
from ..serializers.cartel import (
    CartelSerializer,
    CartelCreateUpdateSerializer,
    ImagenCartelSerializer
)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def listar_carteles(request):
    carteles = Cartel.objects.filter(visible=True).prefetch_related("calles", "imagenes", "tipo")
    serializer = CartelSerializer(carteles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def detalle_cartel(request, pk):
    try:
        cartel = Cartel.objects.prefetch_related("calles", "imagenes", "tipo").get(pk=pk)
    except Cartel.DoesNotExist:
        return Response({"error": "Cartel no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = CartelSerializer(cartel)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@excepcion
def crear_cartel(request):
    serializer = CartelCreateUpdateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cartel = serializer.save(administrador=request.user.persona)
    return Response(CartelSerializer(cartel).data, status=status.HTTP_201_CREATED)

@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def editar_cartel(request, pk):
    try:
        cartel = Cartel.objects.get(pk=pk, administrador=request.user.persona)
    except Cartel.DoesNotExist:
        return Response({"error": "Cartel no encontrado o no autorizado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartelCreateUpdateSerializer(cartel, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(CartelSerializer(cartel).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def eliminar_cartel(request, pk):
    try:
        cartel = Cartel.objects.get(pk=pk, administrador=request.user.persona)
        cartel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Cartel.DoesNotExist:
        return Response({"error": "Cartel no encontrado o no autorizado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def agregar_imagen_cartel(request, pk):
    try:
        cartel = Cartel.objects.get(pk=pk, administrador=request.user.persona)
    except Cartel.DoesNotExist:
        return Response({"error": "Cartel no encontrado o no autorizado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ImagenCartelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(cartel=cartel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
