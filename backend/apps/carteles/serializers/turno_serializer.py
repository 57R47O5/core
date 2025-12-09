from rest_framework import serializers
from apps.carteles.models.turno import Turno
from apps.base.serializers import UsuarioMedicoSerializer
from .paciente_serializer import PacienteSerializer

class TurnoCreateSerializer(serializers.ModelSerializer):
    
    fecha_inicio = serializers.DateTimeField(write_only=True)

    class Meta:
        model = Turno
        fields = "__all__"

class TurnoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    odontologo = UsuarioMedicoSerializer(read_only=True)

    class Meta:
        model = Turno
        fields = "__all__"

class TurnoListSerializer(serializers.ModelSerializer):
    paciente = serializers.CharField(source="paciente.nombre", read_only=True)
    odontologo = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Turno
        fields = ["id", "fecha_inicio", "fecha_fin", "estado", "paciente", "odontologo"]

    def to_representation(self, instance:Turno):
        data = super().to_representation(instance)

        # Convertir a naive (sin tzinfo)
        if instance.fecha_inicio:
            data["fecha_inicio"] = instance.fecha_inicio.replace(tzinfo=None).date().isoformat()

        if instance.fecha_fin:
            data["fecha_fin"] = instance.fecha_fin.replace(tzinfo=None).date().isoformat()

        return data
