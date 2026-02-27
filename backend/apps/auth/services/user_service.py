from framework.security.passwords import hash_password
from framework.exceptions import ExcepcionValidacion
from framework.constantes.mensajes_error import MensajesError
from apps.auth.models.user import User

class UsernameError(MensajesError):
    OBLIGATORIO="El username es obligatorio."
    EXISTENTE="El username ya existe."

class PasswordError(MensajesError):
    OBLIGATORIO="La contraseña es obligatoria."

class UserService:

    @staticmethod
    def create_user(username: str, email: str, password: str):
        if not username:
            raise ExcepcionValidacion(UsernameError.OBLIGATORIO)

        if not password:
            raise ExcepcionValidacion(PasswordError.OBLIGATORIO)

        if User.objects.filter(username=username).exists():
            raise ExcepcionValidacion(UsernameError.EXISTENTE)

        user = User.objects.create(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )

        return user