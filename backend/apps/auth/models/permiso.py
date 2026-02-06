from django.db import models
from framework.models.basemodels import ConstantModel, ComposableManager

class PermisoManager(ComposableManager):
    """
    Manager que expone permisos como constantes del dominio.
    Cada App debe heredar de este Manager
    class PermisosBase(PermisoManager):
        BASE_PERSONA_VIEW = Constant("base.persona.view")
        BASE_PERSONA_EDIT = Constant("base.persona.edit")
        BASE_EMPRESA_VIEW = Constant("base.empresa.view")
    """
    ...
class Permiso(ConstantModel):
    """
    Permiso atómico del sistema.

    Representa una capacidad puntual del dominio que puede ser
    asignada a roles y evaluada por controllers, menús y lógica
    de autorización.

    La identidad del permiso está dada por su `codigo`, no por su ID.
    """

    objects = PermisoManager()
    class Meta:
        managed = False
        db_table = "permiso"
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"

    def __str__(self):
        return self.codigo
