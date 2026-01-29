from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_juridica import PersonaJuridica, Persona
from apps.base.models.documento_identidad import DocumentoIdentidad, TipoDocumentoIdentidad
from apps.base.serializers.documento_identidad_serializer import DocumentoIdentidadCreateSerializer

class PersonaJuridicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaJuridica
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "razon_social", "nombre_fantasia"
        ]


class PersonaJuridicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaJuridica
        fields = ["razon_social", "nombre_fantasia"]
    
    @atomic
    def create(self, validated_data):
        persona=Persona.objects.create()
        instancia = PersonaJuridica.objects.create(
            persona=persona,
            **validated_data)
        return instancia


class PersonaJuridicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaJuridica
        fields = "__all__"


class PersonaJuridicaRetrieveSerializer(PersonaJuridicaSerializer):
    pass

class PersonaJuridicaInputSerializer(serializers.Serializer):
    razon_social = serializers.CharField()
    nombre_fantasia = serializers.CharField()

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

        instancia = PersonaJuridica.objects.create(
            persona=persona,
            **validated_data
        )

        return instancia
    
    def validate_tipo(self, value):
        if value != TipoDocumentoIdentidad.objects.RUC.pk:
            raise serializers.ValidationError("Tipo de documento inválido para personajurídica")
        return value