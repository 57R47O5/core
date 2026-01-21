from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.models.user import User

from framework.exceptions import ExcepcionValidacion
from framework.constantes.mensajes_error import MensajesError

class UsernameError(MensajesError):
    OBLIGATORIO="El username es obligatorio."
    EXISTENTE="El username ya existe."

class PasswordError(MensajesError):
    OBLIGATORIO="La contraseña es obligatoria."


class RegisterView(APIView):
    """
    Registra un nuevo usuario en el sistema.
    """

    def post(self, request):
        data = request.data or {}

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username:
            raise ExcepcionValidacion(UsernameError.OBLIGATORIO)

        if not password:
            raise ExcepcionValidacion(PasswordError.OBLIGATORIO)

        if User.objects.filter(username=username).exists():
            raise ExcepcionValidacion(UsernameError.EXISTENTE)

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
        )

        return Response(
            {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

