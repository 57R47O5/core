from django.db.transaction import atomic
from rest_framework import serializers
from apps.auth.models.user import User
from apps.base.models.persona_fisica import PersonaFisica, Persona

class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer especial. Lo utilizamos para crear usuarios en sistemas
    que requieren creación
    '''
    pass