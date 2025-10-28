from rest_framework import serializers
from ..models.imagencartel import ImagenCartel

class ImagenCartelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenCartel
        fields = ["id", "imagen", "descripcion", "orden"]