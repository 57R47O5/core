import uuid
from django.contrib.gis.db import models
from framework.models.basemodels import BaseModel
from framework.constantes.mensajes_error import MensajesError
from framework.exceptions import ExcepcionValidacion
from apps.geo.models.geo_nivel import GeoNivel, GeoNivelManager

class ErrorLugar(MensajesError):
    NIVEL_INVALIDO="Nivel inválido para la jerarquía geográfica"
    GEOMETRIA_PUNTO="Un Punto debe tener geometría Point"

class Lugar(BaseModel):
    '''
    Clase básica para lugares. 
    Puede referirse a cualquier lugar, desde un país a un punto
    '''
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    codigo = models.CharField(
        max_length=50,
        unique=True
    )

    nombre = models.CharField(
        max_length=255
    )

    tipo = models.CharField(
        max_length=50
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    geom = models.GeometryField(
        srid=4326
    )

    centroide = models.PointField(
        srid=4326,
        geography=True
    )

    padre = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="hijos",
        null=True,
        blank=True
    )

    nivel = models.ForeignKey(GeoNivel, on_delete=models.PROTECT,
        blank=False, null=False)

    activo = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "lugar"
        managed = False
        indexes = [
            models.Index(fields=["tipo"]),
            models.Index(fields=["codigo"]),
            models.Index(fields=["nivel"]),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
    def clean(self):
        if self.padre:
            if self.padre.nivel.order >= self.nivel.order:
                raise ExcepcionValidacion(ErrorLugar.NIVEL_INVALIDO)
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

class PuntoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            nivel=GeoNivelManager.PUNTO
        )

class Punto(Lugar):
    '''
    Proxy model utilizado para registrar puntos
    Pensado específicamente para registrar desde
    la ubicación del usuario
    '''
    objects = PuntoManager()

    class Meta:
        proxy = True
        verbose_name = "Punto"
        verbose_name_plural = "Puntos"

    def save(self, *args, **kwargs):
        self.nivel = GeoNivelManager.PUNTO

        if self.geom and self.geom.geom_type != "Point":
            raise ExcepcionValidacion(ErrorLugar.GEOMETRIA_PUNTO)

        super().save(*args, **kwargs)