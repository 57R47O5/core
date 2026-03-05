from rest_framework import serializers
from apps.auth.models.rol_permiso import RolPermiso
from apps.auth.models.rol import Rol
from apps.auth.models.permiso import Permiso


class RolLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Rol
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "rol"

    def get_label(self, obj:RolPermiso):
        return str(obj)


class PermisoLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Permiso
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "permiso"

    def get_label(self, obj:RolPermiso):
        return str(obj)

class RolPermisoSerializer(serializers.ModelSerializer):
    rol = RolLinkSerializer()
    permiso = PermisoLinkSerializer()

    class Meta:
        model = RolPermiso
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "rol", "permiso"
        ]


class RolPermisoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPermiso
        fields = "__all__"
    pass


class RolPermisoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPermiso
        fields = "__all__"


class RolPermisoRetrieveSerializer(RolPermisoSerializer):
    pass
