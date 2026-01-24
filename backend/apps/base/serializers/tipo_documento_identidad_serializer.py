from rest_framework import serializers
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad

class TipoDocumentoIdentidadSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = TipoDocumentoIdentidad
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class TipoDocumentoIdentidadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumentoIdentidad
        fields = "__all__"
    pass


class TipoDocumentoIdentidadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumentoIdentidad
        fields = "__all__"


class TipoDocumentoIdentidadRetrieveSerializer(TipoDocumentoIdentidadSerializer):
    pass
