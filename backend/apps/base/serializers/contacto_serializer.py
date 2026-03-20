from rest_framework import serializers
from apps.base.models.contacto import Contacto
from apps.base.models.persona import Persona
from apps.base.models.tipo_contacto import TipoContacto


class PersonaLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "persona"

    def get_label(self, obj:Contacto):
        return str(obj)


class TipoContactoLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = TipoContacto
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "tipo-contacto"

    def get_label(self, obj:Contacto):
        return str(obj)

class ContactoSerializer(serializers.ModelSerializer):
    persona = PersonaLinkSerializer()
    tipo = TipoContactoLinkSerializer()

    class Meta:
        model = Contacto
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "tipo"
        ]


class ContactoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = "__all__"
    pass


class ContactoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = "__all__"


class ContactoRetrieveSerializer(ContactoSerializer):
    pass
