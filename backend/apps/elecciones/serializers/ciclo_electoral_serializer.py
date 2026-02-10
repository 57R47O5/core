from rest_framework import serializers
from apps.elecciones.models.ciclo_electoral import CicloElectoral

class CicloElectoralSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = CicloElectoral
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class CicloElectoralCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloElectoral
        fields = "__all__"
    pass


class CicloElectoralUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloElectoral
        fields = "__all__"


class CicloElectoralRetrieveSerializer(CicloElectoralSerializer):
    pass
