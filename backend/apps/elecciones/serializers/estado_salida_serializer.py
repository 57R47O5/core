from rest_framework import serializers
from apps.elecciones.models.estado_salida import EstadoSalida

class EstadoSalidaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = EstadoSalida
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class EstadoSalidaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoSalida
        fields = "__all__"
    pass


class EstadoSalidaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoSalida
        fields = "__all__"


class EstadoSalidaRetrieveSerializer(EstadoSalidaSerializer):
    pass
