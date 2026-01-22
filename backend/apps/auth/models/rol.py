from django.db import models

class Rol(models.Model):
    """
    Rol del sistema.
    Agrupa permisos.
    No contiene lógica de autorización.
    """

    # Identidad del rol
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Identificador estable del rol (ej: admin, user, readonly)"
    )

    name = models.CharField(
        max_length=100,
        help_text="Nombre legible del rol"
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción funcional del rol"
    )

    # Estado
    is_system = models.BooleanField(
        default=False,
        help_text="Indica si es un rol del sistema (no editable por usuarios)"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Permite desactivar el rol sin eliminarlo"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "role"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self) -> str:
        return self.code
