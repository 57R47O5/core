from rest_framework import serializers
from apps.carteles.models.paciente import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            'id',
            'nombre',
            'apellido',
            'dni',
            'telefono',
            'email',
            'notas',
            'fecha_creacion',
        ]
        read_only_fields = ['fecha_creacion']

class PacienteCreateSerializer(PacienteSerializer):
    pass

class PacienteUpdateSerializer(PacienteSerializer):
    pass

class PacienteRetrieveSerializer(PacienteSerializer):
    pass
