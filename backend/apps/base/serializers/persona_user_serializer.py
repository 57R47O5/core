from rest_framework import serializers
from apps.base.models.persona_user import PersonaUser
from apps.base.models.persona import Persona
from apps.auth.models.user import User


class PersonaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "persona"


class UserLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "user"

class PersonaUserSerializer(serializers.ModelSerializer):
    persona = PersonaLinkSerializer()
    user = UserLinkSerializer()

    class Meta:
        model = PersonaUser
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "user", "principal"
        ]


class PersonaUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaUser
        fields = "__all__"
    pass


class PersonaUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaUser
        fields = "__all__"


class PersonaUserRetrieveSerializer(PersonaUserSerializer):
    pass
