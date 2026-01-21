from auth.models.token import Token
from framework.exceptions import ExcepcionAutenticacion
from framework.constantes.mensajes_error import MensajesError

class TokenError(MensajesError):
    MALFORMADO="Token malformado"
    INVALIDO="Token inválido"
    EXPIRADO="Token expirado"

class UsuarioError(MensajesError):
    INACTIVO="Usuario Inactivo"

class AuthTokenMiddleware:
    """
    Middleware de autenticación por token.

    Resuelve la identidad técnica del request a partir del header:
    Authorization: Bearer <token>

    - Inyecta request.user y request.token si el token es válido
    - Si no hay token, deja request.user = None
    - Si el token es inválido, lanza ExcepcionAutenticacion
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None
        request.token = None

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return self.get_response(request)

        token_key = self._extract_token(auth_header)
        token = self._validate_token(token_key)

        request.user = token.user
        request.token = token

        return self.get_response(request)

    def _extract_token(self, auth_header: str) -> str:
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise ExcepcionAutenticacion(
                TokenError.MALFORMADO
            )

        return parts[1]

    def _validate_token(self, token_key: str) -> Token:
        try:
            token = Token.objects.select_related("user").get(
                key=token_key,
                is_active=True,
            )
        except Token.DoesNotExist:
            raise ExcepcionAutenticacion(
                TokenError.INVALIDO
            )

        if token.is_expired():
            raise ExcepcionAutenticacion(
                TokenError.EXPIRADO
            )

        if not token.user.is_active:
            raise ExcepcionAutenticacion(
                UsuarioError.INACTIVO
            )

        return token
