from django.db import models
from framework.models.basemodels import ConstantModel

class Permiso(ConstantModel):
    """
    Permiso atómico del sistema.

    Representa una capacidad puntual del dominio que puede ser
    asignada a roles y evaluada por controllers, menús y lógica
    de autorización.

    La identidad del permiso está dada por su `codigo`, no por su ID.
    """

    class Meta:
        db_table = "permiso"
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"

    def __str__(self):
        return self.codigo
