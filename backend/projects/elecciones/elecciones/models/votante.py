from django.contrib.gis.db import models as gis_models
from django.db import models
from .....geografia.models.distrito import Distrito

class Votante(models.Model):
    """
    Registro del padrón. Tabla tratada como inmutable (solo cargas).
    - Si la fuente trae un id propio (ej: padron_id), úsalo.
    - Incluye geolocalización si está disponible.
    """
    id = models.BigAutoField(primary_key=True)
    padron_uid = models.CharField(max_length=100, db_index=True, null=True, blank=True)  # id origen si aplica
    dni = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    nombre = models.CharField(max_length=200, db_index=True)
    apellido = models.CharField(max_length=200, db_index=True)
    full_name = models.TextField(help_text="nombre + apellido concatenado", db_index=False)
    district = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name="padron_entries")
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    geom = gis_models.PointField(null=True, blank=True, srid=4326)  # coordenadas
    imported_at = models.DateTimeField(auto_now_add=True)
    import_batch = models.CharField(max_length=100, null=True, blank=True)  # referencia a la carga

    class Meta:
        verbose_name = "PadronEntry"
        verbose_name_plural = "PadronEntries"
        indexes = [
            models.Index(fields=['dni'], name='idx_padron_dni'),
            models.Index(fields=['district'], name='idx_padron_district'),
            models.Index(fields=['phone'], name='idx_padron_phone'),
            # trigram search index needs to be created via migration/RunSQL for gin_trgm_ops
        ]

    def save(self, *args, **kwargs):
        # mantener full_name consistente
        self.full_name = f"{self.nombre} {self.apellido}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.dni})"

