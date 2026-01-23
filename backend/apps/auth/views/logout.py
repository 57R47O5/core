from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from framework.exceptions import ExcepcionPermisos
from framework.constantes.mensajes_error import MensajesError
from apps.auth.models import Token

class TokenError(MensajesError):
    NO_VALIDO = "Token inválido o inexistente."

class LogoutView(APIView):
    """
    Logout del usuario autenticado.
    Invalida el token actual.
    """

    def post(self, request):
        token:Token = request.auth

        if not token:
            raise ExcepcionPermisos(TokenError.NO_VALIDO)

        token.delete()

        return Response(
            {
                "mensaje": "Logout exitoso."
            },
            status=status.HTTP_200_OK,
        )
