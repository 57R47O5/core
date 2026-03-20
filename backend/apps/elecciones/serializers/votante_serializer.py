from django.db.transaction import atomic
from rest_framework import serializers
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.votante import Votante
from apps.elecciones.models.campana import Campana
from apps.geo.models.lugar import Punto
from apps.elecciones.models.seccional import Seccional
from apps.base.serializers.persona_fisica_serializer import (
    PersonaFisicaInputSerializer,
    )

class PersonaFisicaLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = PersonaFisica
        fields = ["id", "label", "controller"]

    def get_controller(self, obj:PersonaFisica):
        return "persona-fisica"
    
    def get_label(self, obj: PersonaFisica):
        return obj.nombre_completo

class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Punto
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "lugar"


class SeccionalLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Seccional
        fields = ["id", "nombre", "controller"]

    def get_controller(self, obj):
        return "seccional"

class VotanteSerializer(serializers.ModelSerializer):
    persona = PersonaFisicaLinkSerializer()
    # distrito = LugarLinkSerializer()
    seccional = SeccionalLinkSerializer()

    class Meta:
        model = Votante
        fields = [
            "id", "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "persona", "seccional"
        ]


class VotanteCreateSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField()
    apellidos = serializers.CharField()
    fecha_nacimiento = serializers.DateField()
    class Meta:
        model = Votante
        fields = ["nombres", "apellidos", "fecha_nacimiento"]
    
    @atomic
    def create(self, validated_data):
        persona_fisica = PersonaFisicaInputSerializer().create(validated_data)
        distrito=Campana.objects.last().distrito
        votante = Votante.objects.create(
            persona=persona_fisica,
            distrito=distrito,

        )

        return votante


class VotanteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = "__all__"


class VotanteRetrieveSerializer(VotanteSerializer):
    nombres = serializers.CharField(source="persona.nombres")
    apellidos = serializers.CharField(source="persona.apellidos")
    fecha_nacimiento = serializers.DateField(source="persona.fecha_nacimiento")
    persona_id=serializers.IntegerField(source="persona.id")

    class Meta:
        model = Votante
        fields = "__all__"
