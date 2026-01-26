from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_fisica import PersonaFisica, Persona
class PersonaFisicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaFisica
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "nombres", "apellidos", "fecha_nacimiento"
        ]



class PersonaFisicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento"]

    @atomic
    def create(self, validated_data):
        persona=Persona.objects.create()
        instancia = PersonaFisica.objects.create(
            persona=persona,
            **validated_data)
        return instancia


class PersonaFisicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento"]


class PersonaFisicaRetrieveSerializer(PersonaFisicaSerializer):
    pass
