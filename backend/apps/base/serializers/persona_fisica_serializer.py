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


class PersonaFisicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = ["nombres", "apellidos", "fecha_nacimiento"]


class PersonaFisicaRetrieveSerializer(PersonaFisicaSerializer):
    documentos_identidad = serializers.ReadOnlyField()
    class Meta:
        model = PersonaFisica
        fields = ["persona_id", "nombres", "apellidos", "fecha_nacimiento", "documentos_identidad"]

class PersonaFisicaInputSerializer(serializers.Serializer):
    nombres = serializers.CharField()
    apellidos = serializers.CharField()
    fecha_nacimiento = serializers.DateField()

    @atomic
    def create(self, validated_data):        

        persona = Persona.objects.create()

        instancia = PersonaFisica.objects.create(
            persona=persona,
            **validated_data
        )

        return instancia