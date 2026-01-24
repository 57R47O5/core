from rest_framework import serializers
from apps.base.models.persona import Persona

class PersonaSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Persona
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat"
        ]


class PersonaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"
    pass


class PersonaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"


class PersonaRetrieveSerializer(PersonaSerializer):
    pass
