from rest_framework import serializers
from apps.base.models.tipo_contacto import TipoContacto

class TipoContactoSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = TipoContacto
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "nombre", "descripcion", "codigo", "activo"
        ]


class TipoContactoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoContacto
        fields = "__all__"
    pass


class TipoContactoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoContacto
        fields = "__all__"


class TipoContactoRetrieveSerializer(TipoContactoSerializer):
    pass
