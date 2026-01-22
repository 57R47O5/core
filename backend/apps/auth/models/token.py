from django.db import models
from framework.models.basemodels import BaseModel, SAFEDELETE_PROTECT
from .user import User

class Token(BaseModel):
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

    class Meta:
        db_table = "token"
        managed = False

    def __str__(self):
        return f"Token({self.user_id})"
