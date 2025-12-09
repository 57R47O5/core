from django.contrib.gis.db import models as gis_models
from django.db import models
import uuid

class Distrito(models.Model):
    """
    Distritos donde operan las campañas.
    Puede tener una geometría (polígono) para operaciones territoriales.
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50, blank=True, null=True, help_text="Código oficial del distrito")
    geom = gis_models.PolygonField(null=True, blank=True, srid=4326)

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"

    def __str__(self):
        return self.name



class Person(models.Model):
    """
    Persona base. Puede ser candidato, colaborador, etc.
    """
    id = models.BigAutoField(primary_key=True)
    dni = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['dni'], name='idx_person_dni'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



