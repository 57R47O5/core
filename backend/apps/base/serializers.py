from django.contrib.auth.models import User
from rest_framework import serializers

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
            password=validated_data['password']
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
