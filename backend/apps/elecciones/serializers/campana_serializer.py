from rest_framework import serializers
from apps.elecciones.models.campana import Campana
from apps.base.models.persona_fisica import PersonaFisica
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.ciclo_electoral import CicloElectoral


class PersonaFisicaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = PersonaFisica
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "persona-fisica"


class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "lugar"


class CicloElectoralLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = CicloElectoral
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "ciclo-electoral"

class CampanaSerializer(serializers.ModelSerializer):
    candidato = PersonaFisicaLinkSerializer()
    distrito = LugarLinkSerializer()
    ciclo = CicloElectoralLinkSerializer()

    class Meta:
        model = Campana
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "candidato", "cargo", "distrito", "ciclo", "fecha_inicio", "fecha_fin"
        ]


class CampanaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campana
        fields = "__all__"
    pass


class CampanaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campana
        fields = "__all__"


class CampanaRetrieveSerializer(CampanaSerializer):
    pass
