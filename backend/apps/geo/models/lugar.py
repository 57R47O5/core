import uuid
from decimal import Decimal
from django.db import models
from framework.models.basemodels import BaseModel
from framework.constantes.mensajes_error import MensajesError
from framework.exceptions import ExcepcionValidacion
from apps.geo.models.geo_nivel import GeoNivel, GeoNivelManager
from apps.geo.framework.geometries import Geometry, Point

class ErrorLugar(MensajesError):
    NIVEL_INVALIDO="Nivel inválido para la jerarquía geográfica"
    GEOMETRIA_PUNTO="Un Punto debe tener geometría Point"

class Lugar(BaseModel):
    """
    Clase básica para lugares.
    Puede referirse a cualquier entidad geográfica:
    país, departamento, distrito, barrio o punto.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 🔹 Geometría estructurada (Polygon, MultiPolygon, etc)
    geometry_data = models.JSONField(
        null=True,
        blank=True
    )

    # 🔹 Centroide persistido como lat/lon simples
    centroide_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    centroide_lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    padre = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="hijos",
        db_column="padre",
        null=True,
        blank=True
    )
    tipo = models.CharField(default="Punto")
    nivel = models.ForeignKey(
        GeoNivel,
        on_delete=models.PROTECT,
        db_column="nivel"
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lugar"
        managed = False
        indexes = [
            models.Index(fields=["nivel"]),
        ]

    def __str__(self):
        return f"{self.descripcion}"

    @property
    def geometry(self) -> Geometry | None:
        if not self.geometry_data:
            return None
        return Geometry.from_geojson(self.geometry_data)

    @geometry.setter
    def geometry(self, value: Geometry | None):
        if value is None:
            self.geometry_data = None
        else:
            self.geometry_data = value.to_geojson()


    @property
    def centroide(self) -> Point | None:
        if self.centroide_lat is None or self.centroide_lon is None:
            return None
        return Point(
            lat=self.centroide_lat,
            lon=self.centroide_lon
        )

    @centroide.setter
    def centroide(self, value: Point | None):
        if value is None:
            self.centroide_lat = None
            self.centroide_lon = None
        else:
            self.centroide_lat = Decimal(value.lat)
            self.centroide_lon = Decimal(value.lon)


class PuntoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            nivel=GeoNivel.objects.PUNTO.pk
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
        self.nivel = GeoNivel.objects.PUNTO

        if self.geometry:
            if self.geometry.type != "Point":
                raise ExcepcionValidacion(ErrorLugar.GEOMETRIA_PUNTO)

        super().save(*args, **kwargs)
