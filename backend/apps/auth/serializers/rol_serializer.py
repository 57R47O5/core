from rest_framework import serializers
from apps.auth.models.rol import Rol

class RolSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Rol
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class RolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"
    pass


class RolUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class RolRetrieveSerializer(RolSerializer):
    pass
