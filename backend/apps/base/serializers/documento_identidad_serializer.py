from rest_framework import serializers
from apps.base.models.documento_identidad import DocumentoIdentidad
from apps.base.models.persona import Persona
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad


class PersonaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "persona"


class TipoDocumentoIdentidadLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = TipoDocumentoIdentidad
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "tipo-documento-identidad"

class DocumentoIdentidadSerializer(serializers.ModelSerializer):
    persona = PersonaLinkSerializer()
    tipo = TipoDocumentoIdentidadLinkSerializer()

    class Meta:
        model = DocumentoIdentidad
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "tipo", "numero", "pais_emision", "vigente"
        ]


class DocumentoIdentidadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoIdentidad
        fields = "__all__"
    pass


class DocumentoIdentidadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoIdentidad
        fields = "__all__"


class DocumentoIdentidadRetrieveSerializer(DocumentoIdentidadSerializer):
    pass
