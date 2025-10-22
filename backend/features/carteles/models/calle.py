from django.db import models


class Calle(models.Model):
    """Catálogo de calles para asociar direcciones de carteles."""
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre