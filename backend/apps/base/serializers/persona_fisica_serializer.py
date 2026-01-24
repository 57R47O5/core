from rest_framework import serializers
from apps.base.models.persona_fisica import PersonaFisica

class PersonaFisicaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = PersonaFisica
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "nombres", "apellidos", "fecha_nacimiento"
        ]


class PersonaFisicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = "__all__"
    pass


class PersonaFisicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaFisica
        fields = "__all__"


class PersonaFisicaRetrieveSerializer(PersonaFisicaSerializer):
    pass
