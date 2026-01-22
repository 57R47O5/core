from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from framework.exceptions import ExcepcionPermisos
from framework.constantes.mensajes_error import MensajesError

class UsuarioError(MensajesError):
    NO_AUTENTICADO="Usuario no autenticado."

from apps.auth.models.user import User

class MeView(APIView):
    """
    Devuelve la información del usuario autenticado.
    """

    def get(self, request):
        user: User = request.user

        if not user or not user.is_authenticated:
            raise ExcepcionPermisos(UsuarioError.NO_AUTENTICADO)

        return Response(
            {
                "id": user.pk,
                "username": user.username,
                "is_system": user.is_system,
            },
            status=status.HTTP_200_OK,
        )
