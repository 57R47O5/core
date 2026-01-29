from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_fisica import PersonaFisica, Persona
from apps.base.models.documento_identidad import DocumentoIdentidad, TipoDocumentoIdentidad

from apps.base.serializers.documento_identidad_serializer import DocumentoIdentidadCreateSerializer
class PersonaFisicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaFisica
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "nombres", "apellidos", "fecha_nacimiento"
        ]


class PersonaFisicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento"]


class PersonaFisicaRetrieveSerializer(PersonaFisicaSerializer):
    documentos_identidad = serializers.ReadOnlyField()
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento", "documentos_identidad"]

class PersonaFisicaInputSerializer(serializers.Serializer):
    nombres = serializers.CharField()
    apellidos = serializers.CharField()
    fecha_nacimiento = serializers.DateField()

    tipo = serializers.FloatField()
    
    numero = serializers.CharField()
    pais_emision = serializers.CharField(required=False, default="PY")

    @atomic
    def create(self, validated_data):
        # separar responsabilidades
        documento_data = {
            "tipo": validated_data.pop("tipo"),
            "numero": validated_data.pop("numero"),
            "pais_emision": validated_data.pop("pais_emision"),
        }

        # 1. validar documento
        documento_serializer = DocumentoIdentidadCreateSerializer(
            data=documento_data
        )
        documento_serializer.is_valid(raise_exception=True)

        # 2. crear agregado
        persona = Persona.objects.create()

        DocumentoIdentidad.objects.create(
            persona=persona,
            **documento_serializer.validated_data
        )

        instancia = PersonaFisica.objects.create(
            persona=persona,
            **validated_data
        )

        return instancia