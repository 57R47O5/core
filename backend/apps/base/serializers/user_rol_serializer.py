from rest_framework import serializers
from backend.apps.auth.models.user_rol import UserRol
from backend.apps.auth.models.user import User
from backend.apps.auth.models.rol import Rol


class UserLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "user"


class RolLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Rol
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "rol"

class UserRolSerializer(serializers.ModelSerializer):
    user = UserLinkSerializer()
    rol = RolLinkSerializer()

    class Meta:
        model = UserRol
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "user", "rol"
        ]


class UserRolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRol
        fields = "__all__"
    pass


class UserRolUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRol
        fields = "__all__"


class UserRolRetrieveSerializer(UserRolSerializer):
    pass
