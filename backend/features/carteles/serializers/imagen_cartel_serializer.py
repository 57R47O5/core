from rest_framework import serializers
from ..models.imagen_cartel import ImagenCartel

class ImagenCartelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenCartel
        fields = ["id", "imagen", "descripcion", "orden"]