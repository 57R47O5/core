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



class PersonaJuridicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaJuridica
        fields = ["razon_social", "nombre_fantasia"]


class PersonaJuridicaRetrieveSerializer(PersonaJuridicaSerializer):
    documentos_identidad = serializers.ReadOnlyField()
    
    class Meta:
        model=  PersonaJuridica
        fields= ["id", "persona_id", "razon_social", "nombre_fantasia", "documentos_identidad"]

class PersonaJuridicaInputSerializer(serializers.Serializer):
    razon_social = serializers.CharField()
    nombre_fantasia = serializers.CharField()

    @atomic
    def create(self, validated_data):      
        instancia = PersonaJuridica.objects.create(
            **validated_data
        )

        return instancia

