from rest_framework import serializers
from apps.elecciones.models.distrito_electoral import DistritoElectoral

class DistritoElectoralSerializer(serializers.ModelSerializer):
    limites = serializers.SerializerMethodField()
    centro = serializers.SerializerMethodField()
    class Meta:
        model = DistritoElectoral
        fields = [
            "id", "is_deleted", "createdby", "updatedby", 
            "createdat", "updatedat", "nombre", "descripcion", 
            "codigo", "activo", "limites", "centro"
        ]

    def get_limites(cls, obj):
        fronteras = obj.fronteras.first() if obj.fronteras.exists() else None
        limites = fronteras.lugar.geometry_data if fronteras else {}
        return limites

    def get_centro(cls, obj):
        fronteras = obj.fronteras.first() if obj.fronteras.exists() else None
        centro = fronteras.lugar.centroide if fronteras else {}
        return {"lat":centro.lat, "lon": centro.lon} if centro else {}


class DistritoElectoralCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistritoElectoral
        fields = "__all__"
    pass


class DistritoElectoralUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistritoElectoral
        fields = "__all__"


class DistritoElectoralRetrieveSerializer(DistritoElectoralSerializer):
    pass
