from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_fisica import PersonaFisica, Persona
class PersonaFisicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaFisica
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "nombres", "apellidos", "fecha_nacimiento"
        ]

    def create(self, validated_data):
        Persona.objects.create()
        instancia = PersonaFisica.objects.create(
            persona=Persona,
            **validated_data)
        return instancia


class PersonaFisicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento"]
    pass


class PersonaFisicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha"]


class PersonaFisicaRetrieveSerializer(PersonaFisicaSerializer):
    pass
