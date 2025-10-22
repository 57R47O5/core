from django.db import models


class TipoCartel(models.Model):
    """Catálogo de tipos de carteles (valla, LED, etc.)."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre