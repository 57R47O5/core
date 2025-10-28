from rest_framework import serializers
from ..models.calle import Calle
from ..models.imagencartel import Cartel
from .tipo_cartel_serializer import TipoCartelSerializer
from .persona_serializer import PersonaSerializer
from .calle_serializer import CalleSerializer
from .imagen_cartel_serializer import ImagenCartelSerializer


class CartelSerializer(serializers.ModelSerializer):
    administrador = PersonaSerializer(read_only=True)
    tipo = TipoCartelSerializer(read_only=True)
    calles = CalleSerializer(many=True, read_only=True)
    imagenes = ImagenCartelSerializer(many=True, read_only=True)

    class Meta:
        model = Cartel
        fields = [
            "id", "administrador", "tipo", "calles",
            "latitud", "longitud", "numero", "direccion_completa",
            "alto_metros", "ancho_metros", "precio_exhibicion",
            "visible", "fecha_alta", "imagenes", "superficie"
        ]

class CartelCreateUpdateSerializer(serializers.ModelSerializer):
    calles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Calle.objects.all(), required=False
    )

    class Meta:
        model = Cartel
        fields = [
            "id", "tipo", "calles", "latitud", "longitud",
            "numero", "direccion_completa", "alto_metros",
            "ancho_metros", "precio_exhibicion", "visible"
        ]
