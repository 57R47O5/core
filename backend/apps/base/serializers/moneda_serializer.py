from rest_framework import serializers
from apps.base.models.moneda import Moneda

class MonedaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Moneda
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo", "simbolo"
        ]


class MonedaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = "__all__"
    pass


class MonedaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = "__all__"


class MonedaRetrieveSerializer(MonedaSerializer):
    pass
