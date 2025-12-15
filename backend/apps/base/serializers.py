from django.apps import apps
from rest_framework import serializers

from apps.base.models.user import User
from apps.auditoria.models import AuditoriaUsuario
from apps.base.framework.permissions import get_roles

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registrar nuevos usuarios.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class UserLookupSerializer(serializers.Serializer):
    """
    Serializer que permite obtener un usuario por email o por pk.
    """
    email = serializers.EmailField(required=False)
    pk = serializers.IntegerField(required=False)

    def validate(self, data):
        email = data.get('email')
        pk = data.get('pk')

        if not email and not pk:
            raise serializers.ValidationError("Debe proporcionar un email o un pk.")

        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe un usuario con los datos proporcionados.")

        self.context['user'] = user
        return data

    def get_user(self):
        """
        Retorna el usuario validado.
        """
        return self.context.get('user')
    
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'activo', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'activo': {'required': False},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        usuario_actor = request.user if request and request.user.is_authenticated else None
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # AUDITORÍA
        AuditoriaUsuario.objects.create(
            usuario=usuario_actor,
            usuario_afectado=user,
            accion="CREAR",
            cambios=validated_data  # campos creados
        )
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'activo', 'password']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'activo': {'required': False},
            'password': {'required': False},
        }

    def update(self, instance, validated_data):
        request = self.context.get("request")
        usuario_actor = request.user if request and request.user.is_authenticated else None

         # ====== CAPTURAR ESTADO ORIGINAL ======
        original = {}
        for field in self.Meta.fields:
            if field != "password":  
                original[field] = getattr(instance, field)

        password = validated_data.pop('password', None)

        # ====== APLICAR CAMBIOS ======
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # ====== DETECTAR DIFERENCIAS ======
        cambios = {}
        for campo, valor_original in original.items():
            valor_nuevo = getattr(instance, campo)
            if valor_original != valor_nuevo:
                cambios[campo] = {
                    "antes": valor_original,
                    "después": valor_nuevo
                }

        # Si la contraseña cambió, registrarlo
        if password:
            cambios["password"] = {"antes": "********", "después": "********"}

        # ====== REGISTRAR AUDITORÍA ======
        if cambios:
            AuditoriaUsuario.objects.create(
                usuario=usuario_actor,
                usuario_afectado=instance,
                accion="EDITAR",
                cambios=cambios
            )

        return instance 
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'nombres', 'apellidos']

class UsuarioMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "nombres", "apellidos", "dni",
            "telefono", "email_contacto", "direccion",
            "matricula", "especialidad", "activo"
        ]


class UsuarioUpdateSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "nombres",
            "apellidos",
            "dni",
            "telefono",
            "direccion",
            "email_contacto",
            "activo",
            "roles",
        ]
        read_only_fields = ["id", "username"]

    def get_roles(self, instancia):
        return get_roles(instancia)