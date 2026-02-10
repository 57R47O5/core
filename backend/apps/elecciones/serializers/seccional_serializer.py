from rest_framework import serializers
from apps.elecciones.models.seccional import Seccional
from apps.geo.models.lugar import Lugar
from apps.elecciones.models.campana import Campana


class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "lugar"


class CampanaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "campana"

class SeccionalSerializer(serializers.ModelSerializer):
    zona = LugarLinkSerializer()
    campana = CampanaLinkSerializer()

    class Meta:
        model = Seccional
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "zona", "campana"
        ]


class SeccionalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccional
        fields = "__all__"
    pass


class SeccionalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccional
        fields = "__all__"


class SeccionalRetrieveSerializer(SeccionalSerializer):
    pass
