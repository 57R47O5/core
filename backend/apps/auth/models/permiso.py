from django.db import models
from framework.models.basemodels import BaseModel

class Permiso(BaseModel):
    """
    Permiso atómico del sistema.
    Define una capacidad puntual que puede ser asignada a uno o más roles.
    """

    code = models.CharField(
        max_length=150,
        unique=True,
        help_text="Identificador único del permiso. Ej: sales.order.create"
    )

    name = models.CharField(
        max_length=100,
        help_text="Nombre corto y legible del permiso"
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descripción funcional del permiso"
    )

    app_label = models.CharField(
        max_length=50,
        help_text="App propietaria del permiso. Ej: sales, inventory"
    )

    class Meta:
        db_table = "permiso"
        managed = False

    def __str__(self):
        return self.code
