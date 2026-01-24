
from django.db import models

from framework.models.basemodels import BaseModel
from apps.auth.models.user import User
from apps.base.models.persona import Persona


class PersonaUser(BaseModel):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="usuarios",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="personas",
    )

    principal = models.BooleanField(default=False)

    class Meta:
        db_table = "persona_user"
        unique_together = ("persona", "user")
        managed = False
