from rest_framework import serializers
from apps.elecciones.models.lugar_distrito import LugarDistrito
from apps.elecciones.models.distrito_electoral import DistritoElectoral
from apps.geo.models.lugar import Lugar


class DistritoElectoralLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = DistritoElectoral
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "distrito-electoral"


class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "lugar"

class LugarDistritoSerializer(serializers.ModelSerializer):
    distrito = DistritoElectoralLinkSerializer()
    lugar = LugarLinkSerializer()

    class Meta:
        model = LugarDistrito
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "distrito", "lugar"
        ]


class LugarDistritoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LugarDistrito
        fields = "__all__"
    pass


class LugarDistritoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LugarDistrito
        fields = "__all__"


class LugarDistritoRetrieveSerializer(LugarDistritoSerializer):
    pass
