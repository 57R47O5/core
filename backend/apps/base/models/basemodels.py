
import logging

from django.db import IntegrityError, models
from django.db.models.deletion import Collector
from safedelete import HARD_DELETE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from safedelete.queryset import SafeDeleteQueryset

from .historicals import NewHistoricalRecords

from .fields import UserForeignKey

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


class NewQuerySet(SafeDeleteQueryset):
    def delete(self, force_policy=None):
        if force_policy == HARD_DELETE:
            # Optimización de HARD_DELETE
            # Elimina todas las instancias en un query (en vez de invocar delete() por cada instancia)

            """Delete the records in the current QuerySet."""
            assert self.query.can_filter(), \
                "Cannot use 'limit' or 'offset' with delete."

            if self._fields is not None:
                raise TypeError("Cannot call delete() after .values() or .values_list()")

            del_query = self._chain()

            # The delete is actually 2 queries - one to find related objects,
            # and one to delete. Make sure that the discovery of related
            # objects is performed on the same database as the deletion.
            del_query._for_write = True

            # Disable non-supported fields.
            del_query.query.select_for_update = False
            del_query.query.select_related = False
            del_query.query.clear_ordering(force_empty=True)

            collector = Collector(using=del_query.db)
            collector.collect(del_query)

            for instances in collector.data.values():
                for obj in instances:
                    setattr(obj, 'history_bulk_delete', True)

            deleted, _rows_count = collector.delete()

            # Clear the result cache, in case this QuerySet gets reused.
            self._result_cache = None
            return deleted, _rows_count
        else:
            super().delete(force_policy)
    delete.alters_data = True


class NewModelManager(SafeDeleteManager):
    _queryset_class = NewQuerySet

class BaseModel(SafeDeleteModel):
    id = models.AutoField(primary_key=True)

    is_deleted = models.BooleanField(
        'Eliminado', editable=False, null=False, blank=False, default=False, db_index=True)
    createdby = UserForeignKey(
        verbose_name="CreatedBy", auto_user_add=True, null=False, editable=False)
    updatedby = UserForeignKey(
        verbose_name="UpdatedBy", auto_user=True, null=False, editable=False,
        related_name="%(app_label)s_%(class)s_updatedby")
    createdat = models.DateTimeField(
        'Creado', auto_now_add=True, editable=False, null=True)
    updatedat = models.DateTimeField(
        'Actualizado', auto_now=True, editable=False, null=True)

    objects = NewModelManager()
    history = NewHistoricalRecords(inherit=True)

    # Django safedelete
    _safedelete_policy = SOFT_DELETE_CASCADE

    def save(self, *args, **kwargs):
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


class BasicModelManager(NewModelManager):
    _queryset_class = NewQuerySet

    def get_queryset(self):
        return super().get_queryset().order_by('nombre')


class BasicModel(BaseModel):
    nombre = models.CharField(
        'Nombre', null=False, blank=False, max_length=200, default='')
    descripcion = models.TextField(
        'Descripcion', null=True, blank=True)

    objects = BasicModelManager()

    class Meta(BaseModel.Meta):
        abstract = True
