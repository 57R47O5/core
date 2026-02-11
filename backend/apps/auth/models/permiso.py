from django.db import models
from framework.models.basemodels import Constant, ConstantModel, ComposableManager

class PermisoGroup:
    '''
    Clase utilizada para agrupar permisos
    '''
    @classmethod
    def constants(cls) -> dict[str, Constant]:
        return {
            name: value
            for name, value in vars(cls).items()
            if isinstance(value, Constant)
        }

    @classmethod
    def all(cls):
        permisos = []

        # 1. permisos propios
        permisos.extend(
            value for value in vars(cls).values()
            if isinstance(value, Constant)
        )

        # 2. permisos de grupos
        for group in getattr(cls, "grupos", []):
            permisos.extend(group.all())

        return permisos
    
    @classmethod
    def _get_groups(cls):
        return getattr(cls, "grupos", [])
class PermisoManager(ComposableManager):
    """
    Manager que expone permisos como constantes del dominio.
    Cada App debe heredar de este Manager
    class PermisosBase(PermisoManager):
        BASE_PERSONA_VIEW = Constant("base.persona.view")
        BASE_PERSONA_EDIT = Constant("base.persona.edit")
        BASE_EMPRESA_VIEW = Constant("base.empresa.view")
    """
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


