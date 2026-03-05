from rest_framework import serializers
from apps.auth.models.user_rol import UserRol
from apps.auth.models.user import User
from apps.auth.models.rol import Rol


class UserLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "user"

    def get_label(self, obj:UserRol):
        return str(obj)


class RolLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Rol
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "rol"

    def get_label(self, obj:UserRol):
        return str(obj)

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
