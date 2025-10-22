from rest_framework import serializers
from ..models.calle import Calle


class CalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calle
        fields = ["id", "nombre"]