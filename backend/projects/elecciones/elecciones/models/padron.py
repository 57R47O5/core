from django.db import models
from django.contrib.postgres.indexes import GinIndex, BTreeIndex
from django.contrib.postgres.search import SearchVectorField

class Padron(models.Model):
    ci = models.CharField(max_length=20, primary_key=True)   # Normalizar: sin guiones, sin puntos
    nombres = models.CharField(max_length=160, db_index=False)
    apellidos = models.CharField(max_length=160, db_index=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    departamento = models.CharField(max_length=100, db_index=False)
    distrito = models.CharField(max_length=120, db_index=False)
    seccional = models.CharField(max_length=50, db_index=False)

    # Campo para búsquedas full-text (creado por migración y mantenido por triggers o actualizaciones manuales)
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        db_table = "padron"
        # Índices declarativos de alto nivel (complementamos con SQL raw en migraciones)
        indexes = [
            BTreeIndex(fields=['departamento', 'distrito', 'seccional'], name='padron_loc_idx'),
            BTreeIndex(fields=['ci'], name='padron_ci_idx'),  # redundante con PK pero explícito si querés
            # GinIndex para SearchVectorField (si usás SearchVectorField)
            GinIndex(fields=['search_vector'], name='padron_search_gin'),
            # Podrías agregar índices funcionales con migración SQL (ej: lower(apellidos))
        ]
