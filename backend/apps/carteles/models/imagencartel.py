from django.db import models
from .cartel import Cartel

class ImagenCartel(models.Model):
    """Permite asociar múltiples imágenes a un cartel."""
    id = models.BigAutoField(primary_key=True)
    cartel = models.ForeignKey(Cartel, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="carteles/")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table='imagen_cartel'
        ordering = ["orden"]

    def __str__(self):
        return f"Imagen de {self.cartel} ({self.orden})"
