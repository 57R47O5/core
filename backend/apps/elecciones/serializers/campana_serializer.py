from django.db.transaction import atomic
from rest_framework import serializers
from apps.elecciones.models.campana import Campana
from apps.base.models.persona_fisica import PersonaFisica
from apps.elecciones.models.distrito_electoral import DistritoElectoral
from apps.elecciones.models.ciclo_electoral import CicloElectoral
from apps.base.serializers.persona_fisica_serializer import PersonaFisicaInputSerializer


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


class DistritoLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = DistritoElectoral
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "lugar"
    
    def get_label(self, obj:DistritoElectoral):
        return str(obj)


class CicloElectoralLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()
    class Meta:
        model = CicloElectoral
        fields = ["id", "label", "controller"]

    def get_controller(self, obj):
        return "ciclo-electoral"
    
    def get_label(self, obj):
        return str(obj)

class CampanaSerializer(serializers.ModelSerializer):
    candidato = PersonaFisicaLinkSerializer()
    distrito = DistritoLinkSerializer()
    ciclo = CicloElectoralLinkSerializer()

    class Meta:
        model = Campana
        fields = [
            "id", "is_deleted", "createdby", "updatedby", "createdat", "updatedat", "candidato", "cargo", "distrito", "ciclo", "fecha_inicio", "fecha_fin"
        ]


class CampanaCreateSerializer(serializers.ModelSerializer):

    candidato=serializers.PrimaryKeyRelatedField(queryset=PersonaFisica.objects.all())
    class Meta:
        model = Campana
        fields = ["candidato", "distrito", "ciclo", "fecha_inicio", "fecha_fin"]
    
    @atomic
    def create(self, validated_data):
        campana=Campana.objects.create(**validated_data)
        return campana


class CampanaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campana
        fields = "__all__"


class CampanaRetrieveSerializer(CampanaSerializer):
    pass
