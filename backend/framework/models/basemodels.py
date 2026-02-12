
import logging

from django.db import IntegrityError, models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from .historicals import ORCHistoricalRecords

from framework.middleware.user_middleware import get_current_username

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# Variables globles
RELOAD_COMPLEX = {}

# BaseModels

def SAFEDELETE_PROTECT(collector, field, sub_objs, using):
    """
    Previene el borrado del objeto referenciado si el objeto
    que posee la referencia no está eliminado lógicamente.

    Integración con django safe-delete.

    Ejemplo de uso:
    ```python
        class Funcionario(BaseModel):
            persona = models.ForeignKey(Persona, on_delete=SAFEDELETE_PROTECT)
            detalle = models.ForeignKey(Persona, on_delete=models.CASCADE)
    ```
    """

    # Si los objetos que posee la referencia son instancias del SafeDeleteModel
    if issubclass(sub_objs.model, SafeDeleteModel):
        # Excluir aquellos que están eliminados lógicamente
        filtered_subobjs = sub_objs.exclude(deleted__isnull=False)
    else:
        filtered_subobjs = sub_objs

    # Si existen objetos que no fueron eliminados lógicamente
    if filtered_subobjs:
        # Lanzar una excepción de ProtectedError
        models.PROTECT(collector, field, filtered_subobjs, using)


class ORCModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

class BaseModel(SoftDeleteModel):
    id = models.AutoField(primary_key=True)

    is_deleted = models.BooleanField(
        'Eliminado', editable=False, null=False, blank=False, default=False, db_index=True)
    createdby = models.CharField(
        'Created by',
        max_length=150,
        null=False,
        editable=False
    )
    updatedby = models.CharField(
        'Updated by',
        max_length=150,
        null=False,
        editable=False
    )
    createdat = models.DateTimeField(
        'Creado', auto_now_add=True, editable=False, null=True)
    updatedat = models.DateTimeField(
        'Actualizado', auto_now=True, editable=False, null=True)

    objects = ORCModelManager()
    history = ORCHistoricalRecords(inherit=True)

    # Django safedelete
    _safedelete_policy = SOFT_DELETE_CASCADE

    # Fks usadas para extensión
    EMBEDDED_FKS = []

    def save(self, *args, **kwargs):
        username = get_current_username()

        if not self.pk:
            self.createdby = username
        self.updatedby = username
        try:
            super().save(*args, **kwargs)
        except IntegrityError as exc:
            if 'UNIQUE constraint'.lower() in str(exc).lower():
                raise IntegrityError('El registro ya existe')
            else:
                raise exc

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['deleted']),
        ]

class BasicModelManager(ORCModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class BasicModel(BaseModel):
    nombre = models.CharField(
        'Nombre', null=False, blank=False, max_length=200, default='')
    descripcion = models.TextField(
        'Descripcion', null=True, blank=True)

    objects = BasicModelManager()

    class Meta(BaseModel.Meta):
        abstract = True

class ConstantModel(BasicModel):
    """
    Modelo base para constantes del dominio.
    Las instancias se identifican por `codigo`, no por ID.
    """
    codigo = models.CharField(
        'Código', max_length=50, unique=True, db_index=True
    )
    activo = models.BooleanField(default=True)

    class Meta(BasicModel.Meta):
        abstract = True

class Constant:
    def __init__(self, codigo):
        self.codigo = codigo
        self._cache = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if RELOAD_COMPLEX.get(self.codigo, False) or self._cache is None:
            self._cache = instance.get(codigo=self.codigo)
            RELOAD_COMPLEX[self.codigo] = False

        return self._cache

class ConstantModelManager(BasicModelManager):
    """
    Manager base para modelos constantes.

    Además de exponer los métodos estándar de acceso a constantes,
    este manager define un ORDEN LÓGICO implícito entre ellas basado
    exclusivamente en el orden de declaración en la clase.

    Importante:
    - El orden NO se persiste en la base de datos.
    - El orden NO forma parte del esquema ni de los changelogs.
    - El orden es puramente lógico y está determinado por el orden
      en que las constantes son definidas en el manager.
    - Modificar el orden implica únicamente reordenar las constantes
      en el código.

    Esto permite expresar jerarquías o comparaciones (por ejemplo,
    validaciones entre niveles) sin introducir complejidad innecesaria
    en el modelo físico.
    """

    @classmethod
    def ordered_constants(cls):
        """
        Retorna las constantes respetando el orden de declaración
        en la clase.
        """
        return list(cls.constants().values())

    @classmethod
    def get_order(cls, codigo):
        """
        Devuelve la posición (índice) lógica de una constante
        según su orden de declaración.
        """
        for index, const in enumerate(cls.ordered_constants()):
            if const.codigo == codigo:
                return index
        raise ValueError("Nivel no encontrado")

class ComposableManager(BasicModelManager):
    """
    Base para artefactos definidos por app pero
    materializados a nivel proyecto.
    """
    __registry__ = []

    @classmethod
    def register(cls, subclass):
        cls.__registry__.append(subclass)

    @classmethod
    def get_definitions(cls):
        return cls.__registry__