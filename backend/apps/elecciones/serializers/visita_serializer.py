from django.db.transaction import atomic
from rest_framework import serializers
from apps.geo.models.lugar import Punto
from apps.elecciones.models.votante import Votante
from apps.elecciones.models.visita import Visita
from apps.elecciones.models.salida import Salida, EstadoSalida
from apps.elecciones.models.resultado_visita import ResultadoVisita
from apps.geo.serializers.lugar_serializer import (
    PuntoInputSerializer,
    )

class SalidaLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Salida
        fields = ["id", "label", "controller"]

    def get_controller(self, obj:Salida):
        return "salida"
    
    def get_label(self, obj: Salida):
        return f"{obj.colaborador.persona.nombres} - {obj.fecha.isoformat()}"
    

class VotanteLinkSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()

    class Meta:
        model = Votante
        fields = ["id", "label", "controller"]

    def get_controller(self, obj:Votante):
        return "votante"
    
    def get_label(self, obj: Votante):
        return obj.persona.nombre_completo

class LugarLinkSerializer(serializers.ModelSerializer):
    controller = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = Punto
        fields = ["id", "nombre", "controller", "centroide_lat", "centroide_lon"]

    def get_controller(self, obj):
        return "lugar"
    
    def get_nombre(self, obj):
        return "nombre"


class VisitaSerializer(serializers.ModelSerializer):
    salida = SalidaLinkSerializer()
    lugar = LugarLinkSerializer()

    class Meta:
        model = Visita
        fields = [
            "id", "id", "is_deleted", "createdby", 
            "updatedby", "createdat", "updatedat", 
            "lugar","persona"
        ]


class VisitaCreateSerializer(serializers.ModelSerializer):
    lugar = PuntoInputSerializer()
    salida = serializers.PrimaryKeyRelatedField(queryset=Salida.objects.filter(estado=EstadoSalida.objects.EN_CURSO))
    resultado = serializers.PrimaryKeyRelatedField(queryset=ResultadoVisita.objects.all())
    votante = serializers.PrimaryKeyRelatedField(queryset=Votante.objects.all())

    class Meta:
        model = Visita
        fields = ["lugar", "salida", "votante", "resultado", "notas"]
    
    @atomic
    def create(self, validated_data):
        datos_lugar=validated_data.pop("lugar")
        lugar = PuntoInputSerializer().create(datos_lugar)
        visita = Visita.objects.create(
            lugar=lugar,
            **validated_data
        )

        return visita


class VisitaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = "__all__"


class VisitaRetrieveSerializer(VisitaSerializer):

    class Meta:
        model = Visita
        fields = "__all__"
