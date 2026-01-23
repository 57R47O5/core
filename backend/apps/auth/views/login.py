from datetime import timedelta
from django.utils import timezone
from framework.security.passwords import verify_password
import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.auth.models.user import User
from apps.auth.models.token import Token

from framework.constantes.mensajes_error import MensajesError
from framework.exceptions import (
    excepcion,
    ExcepcionValidacion,
    ExcepcionAutenticacion,
)

class LoginError(MensajesError):
    JSON_INVALIDO="Payload JSON INVALIDA"
    FALTA_EMAIL_CONTRASENHA="Se requiere email y contraseña"
    CREDENCIALES_INVALIDAS="Credenciales Inválidas"
    USUARIO_INACTIVO="Usuario Inactivo"


class LoginView(APIView):

    @excepcion
    def post(self, request):
        """
        Autentica un usuario y emite un token de acceso.
        """

        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            raise ExcepcionValidacion(LoginError.JSON_INVALIDO)

        identifier = payload.get("identifier")
        password = payload.get("password")

        if not identifier or not password:
            raise ExcepcionValidacion(LoginError.FALTA_EMAIL_CONTRASENHA)

        try:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                user = User.objects.get(email=identifier)

        except User.DoesNotExist:
            raise ExcepcionAutenticacion(LoginError.CREDENCIALES_INVALIDAS)

        if not user.is_active:
            raise ExcepcionAutenticacion(LoginError.USUARIO_INACTIVO)

        if not verify_password(password, user.password_hash):
            raise ExcepcionAutenticacion(LoginError.CREDENCIALES_INVALIDAS)

        expires_at = timezone.now() + timedelta(days=7)

        token = Token.objects.create_token(
                user=user,
                request=request,
                expires_at=expires_at
            )

        return Response(
            {
                "token": token.key,   
                "expires_at": expires_at.isoformat(),
            },
            status=status.HTTP_200_OK
        )
