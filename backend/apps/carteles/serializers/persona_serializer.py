from rest_framework import serializers
from ..models.persona import Persona


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id", "tipo", "nombre", "documento",
            "telefono", "email", "usuario"
        ]