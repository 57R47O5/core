from rest_framework import serializers
from apps.elecciones.models.salida import Salida
from apps.elecciones.models.campana import Campana
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.models.estado_salida import EstadoSalida


class CampanaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "campana"


class ColaboradorLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Colaborador
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "colaborador"


class EstadoSalidaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = EstadoSalida
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "estado-salida"

class SalidaSerializer(serializers.ModelSerializer):
    campana = CampanaLinkSerializer()
    colaborador = ColaboradorLinkSerializer()
    estado = EstadoSalidaLinkSerializer()

    class Meta:
        model = Salida
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "campana", "colaborador", "fecha", "estado"
        ]


class SalidaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = "__all__"
    pass


class SalidaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = "__all__"


class SalidaRetrieveSerializer(SalidaSerializer):
    pass
