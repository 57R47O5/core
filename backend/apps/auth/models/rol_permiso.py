from django.db import models
from framework.models.basemodels import BaseModel, SAFEDELETE_PROTECT
from .rol import Rol
from .permiso import Permiso


class RolPermiso(BaseModel):
    """
    Relación explícita entre Rol y Permiso.
    Define qué acciones puede ejecutar un rol.
    """

    rol = models.ForeignKey(
        Rol,
        on_delete=SAFEDELETE_PROTECT,
        related_name="permisos"
    )

    permiso = models.ForeignKey(
        Permiso,
        on_delete=SAFEDELETE_PROTECT,
        related_name="roles"
    )

    class Meta:
        db_table = "rol_permiso"
        managed = False
        unique_together = ("rol", "permiso")

    def __str__(self):
        return f"{self.rol.code} → {self.permiso.code}"
