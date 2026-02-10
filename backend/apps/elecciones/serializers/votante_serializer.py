from rest_framework import serializers
from apps.elecciones.models.votante import Votante
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.seccional import Seccional


class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "lugar"


class SeccionalLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Seccional
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "seccional"

class VotanteSerializer(serializers.ModelSerializer):
    distrito = LugarLinkSerializer()
    seccional = SeccionalLinkSerializer()

    class Meta:
        model = Votante
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "distrito", "seccional"
        ]


class VotanteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = "__all__"
    pass


class VotanteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = "__all__"


class VotanteRetrieveSerializer(VotanteSerializer):
    pass
