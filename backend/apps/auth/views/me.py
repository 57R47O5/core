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
    Devuelve la información del usuario autenticado
    a partir del token validado por el middleware.
    """

    authentication_classes = []  # importante: NO usar DRF auth
    permission_classes = []

    def get(self, request):
        token = getattr(request, "token", None)

        salida = {
            "user":None
        }
        if token:
            user: User = token.user

            salida = {
                    "id": user.pk,
                    "user": user.username,
                    "is_system": user.is_system,
                }
        

        return Response(
            salida,
            status=status.HTTP_200_OK,
        )