from django.db.transaction import atomic
from rest_framework import serializers
from apps.elecciones.models.colaborador import Colaborador
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.campana import Campana
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaInputSerializer,
    PersonaFisicaUpdateSerializer,
    PersonaFisicaRetrieveSerializer,
    )

class PersonaFisicaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = PersonaFisica
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "persona-fisica"


class CampanaLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "campana"

class ColaboradorSerializer(serializers.ModelSerializer):
    persona = PersonaFisicaLinkSerializer()
    campana = CampanaLinkSerializer()

    class Meta:
        model = Colaborador
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "campana"
        ]


class ColaboradorCreateSerializer(serializers.ModelSerializer):

    persona = PersonaFisicaInputSerializer()
    class Meta:
        model = Colaborador
        fields = "persona"

    @atomic
    def create(self, validated_data):
        persona_data = validated_data.pop("persona")

        persona_serializer = PersonaFisicaInputSerializer(data=persona_data)
        persona_serializer.is_valid(raise_exception=True)
        persona_fisica = persona_serializer.save()

        campana=Campana.objects.last()

        colaborador = Colaborador.objects.create(
            persona=persona_fisica,
            campana=campana
        )

        return colaborador


class ColaboradorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = "__all__"


class ColaboradorRetrieveSerializer(ColaboradorSerializer):
    pass
