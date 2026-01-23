import secrets
from django.db import models
from django.utils import timezone
from framework.models.basemodels import BaseModel, SAFEDELETE_PROTECT
from .user import User

class TokenManager(models.Manager):

    def create_token(
        self,
        *,
        user,
        request=None,
        expires_at=None,
    ):
        """
        Crea un token de autenticación consistente.
        """

        ip_address = None
        user_agent = None

        if request:
            ip_address = self._get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT")

        token = self.model(
            user=user,
            key=self._generate_key(),
            is_active=True,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        token.save(using=self._db)
        return token

    def _generate_key(self) -> str:
        # 64 chars hex → seguro y simple
        return secrets.token_hex(32)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

class Token(models.Model):
    """
    Token de autenticación.
    Representa una sesión explícita y revocable.
    """

    user = models.ForeignKey(
        User,
        on_delete=SAFEDELETE_PROTECT,
        related_name="tokens"
    )

    key = models.CharField(
        max_length=64,
        unique=True,
        help_text="Token de autenticación"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Permite revocar el token sin borrarlo"
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha de expiración del token"
    )

    last_used_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Último uso del token"
    )

    user_agent = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    ip_address = models.CharField(
        max_length=45,
        blank=True,
        null=True
    )

    objects = TokenManager()

    class Meta:
        db_table = "token"
        managed = False

    def __str__(self):
        return f"Token({self.user.pk})"
