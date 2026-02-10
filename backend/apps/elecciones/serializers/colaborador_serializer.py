from rest_framework import serializers
from apps.elecciones.models.colaborador import Colaborador
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.campana import Campana


class PersonaFisicaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = PersonaFisica
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "persona-fisica"


class CampanaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "campana"

class ColaboradorSerializer(serializers.ModelSerializer):
    persona = PersonaFisicaLinkSerializer()
    campana = CampanaLinkSerializer()

    class Meta:
        model = Colaborador
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "campana"
        ]


class ColaboradorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = "__all__"
    pass


class ColaboradorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = "__all__"


class ColaboradorRetrieveSerializer(ColaboradorSerializer):
    pass
