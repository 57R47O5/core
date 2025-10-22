from rest_framework import serializers
from ..models.tipo_cartel import TipoCartel


class TipoCartelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCartel
        fields = ["id", "nombre", "descripcion"]
