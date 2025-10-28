from django.db import models


class Calle(models.Model):
    """Catálogo de calles para asociar direcciones de carteles."""
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table='calle'

    def __str__(self):
        return self.nombre