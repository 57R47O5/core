from django.db.transaction import atomic
from rest_framework import serializers
from apps.auth.models.user import User

class UserSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = User
        fields = [
            "id", "username", "created_at", 
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    ...


class UserRetrieveSerializer(UserSerializer):
    roles = serializers.ReadOnlyField()
    permisos = serializers.ReadOnlyField()
    persona_fisica = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = User
        fields = [
            "id", "username", "created_at", "roles",
            "permisos", "persona_fisica", "is_active"
        ]

    def get_persona_fisica(self, obj:User):
        datos_persona_fisica = {}
        persona_fisica = obj.persona.persona.fisica if obj.persona else None
        if persona_fisica:
            datos_persona_fisica = {
                "id": persona_fisica.pk,
                "nombres": str(persona_fisica)
            }
        return datos_persona_fisica

class UserInputSerializer(serializers.Serializer):
    ...