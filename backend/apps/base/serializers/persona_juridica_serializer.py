from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_juridica import PersonaJuridica, Persona

class PersonaJuridicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaJuridica
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "razon_social", "nombre_fantasia"
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
