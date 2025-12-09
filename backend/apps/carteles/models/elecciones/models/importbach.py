from django.db import models

class ImportBatch(models.Model):
    """
    Registro de importaciones del padrón para trazabilidad.
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=300, null=True, blank=True)
    rows_total = models.IntegerField(null=True, blank=True)
    rows_loaded = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default='completed')  # started, running, failed, completed
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Import {self.name} ({self.created_at})"