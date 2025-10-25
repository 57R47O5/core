from enum import Enum
from django.db import models
from .persona import Persona
from .tipo_cartel import TipoCartel
from .calle import Calle


class Cartel(models.Model):
    """Cartel físico con ubicación y datos asociados."""

    class Estado(Enum):
        DISPONIBLE='D'
        OCUPADO = 'O'
        INACTIVO='I'

        @classmethod
        def choices(cls):
            return [(estado.value, estado.name) for estado in cls]

    administrador = models.ForeignKey(Persona, on_delete=models.SET_NULL, 
        related_name="carteles", blank=True, null=True)
    tipo = models.ForeignKey(TipoCartel, on_delete=models.SET_NULL, 
        null=True, related_name="carteles")
    estado = models.CharField(max_length=1, choices=Estado.choices(), 
        blank=True, null=True)

    calles = models.ManyToManyField(Calle, related_name="carteles", blank=True)

    latitud = models.DecimalField(max_digits=21, decimal_places=18)
    longitud = models.DecimalField(max_digits=21, decimal_places=18)

    numero = models.CharField(max_length=20, blank=True, null=True)
    direccion_completa = models.CharField(max_length=255, blank=True, null=True)

    alto_metros = models.DecimalField(max_digits=5, decimal_places=2)
    ancho_metros = models.DecimalField(max_digits=5, decimal_places=2)

    precio_exhibicion = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    visible = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        calles_str = ", ".join(calle.nombre for calle in self.calles.all()[:2])
        return f"{self.tipo} - {calles_str or 'Ubicación sin calles'}"

    @property
    def superficie(self):
        """Calcula el área del cartel en m²."""
        return self.alto_metros * self.ancho_metros