from rest_framework import serializers
from apps.elecciones.models.distrito_electoral import DistritoElectoral

class DistritoElectoralSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = DistritoElectoral
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


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
