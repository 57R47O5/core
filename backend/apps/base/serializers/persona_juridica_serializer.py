from rest_framework import serializers
from apps.base.models.persona_juridica import PersonaJuridica

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
        fields = "__all__"
    pass


class PersonaJuridicaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaJuridica
        fields = "__all__"


class PersonaJuridicaRetrieveSerializer(PersonaJuridicaSerializer):
    pass
