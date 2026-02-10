from rest_framework import serializers
from apps.elecciones.models.resultado_visita import ResultadoVisita

class ResultadoVisitaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = ResultadoVisita
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo", "valor"
        ]


class ResultadoVisitaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoVisita
        fields = "__all__"
    pass


class ResultadoVisitaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoVisita
        fields = "__all__"


class ResultadoVisitaRetrieveSerializer(ResultadoVisitaSerializer):
    pass
