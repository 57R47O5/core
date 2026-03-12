from datetime import date
from rest_framework import serializers
from apps.elecciones.models.salida import Salida
from apps.elecciones.models.campana import Campana
from apps.elecciones.models.colaborador import Colaborador
from apps.elecciones.models.estado_salida import EstadoSalida


class CampanaLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "campana"
    
    def get_label(self, obj: Campana):
        return str(obj)


class ColaboradorLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Colaborador
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "colaborador"
    
    def get_label(self, obj: Colaborador):
        return str(obj)


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
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "campana", "colaborador", "fecha", "estado"
        ]


class SalidaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = "__all__"
    pass


class SalidaUpdateSerializer(serializers.ModelSerializer):
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoSalida.objects.all())
    class Meta:
        model = Salida
        fields = ["fecha", "estado"]

    def update(self, instance: Salida, validated_data):
        instance.fecha = validated_data.get("fecha")
        instance.estado = validated_data.get("estado")
        instance.save()
        return instance


class SalidaRetrieveSerializer(SalidaSerializer):
    pass
