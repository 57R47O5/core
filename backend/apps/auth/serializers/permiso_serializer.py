from rest_framework import serializers
from apps.auth.models.permiso import Permiso

class PermisoSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Permiso
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class PermisoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = "__all__"
    pass


class PermisoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = "__all__"


class PermisoRetrieveSerializer(PermisoSerializer):
    pass
