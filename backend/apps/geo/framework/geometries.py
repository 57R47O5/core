from dataclasses import dataclass
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2
from typing import List, Union
from django.db import models


@dataclass(frozen=True)
class Geometry:
    type: str
    coordinates: Union[list, list[list], list[list[list]]]

    VALID_TYPES = {
        "Point",
        "LineString",
        "Polygon",
        "MultiPolygon",
    }

    def __post_init__(self):
        if self.type not in self.VALID_TYPES:
            raise ValueError(f"Invalid geometry type: {self.type}")

    def to_geojson(self) -> dict:
        return {
            "type": self.type,
            "coordinates": self.coordinates,
        }

    @classmethod
    def from_geojson(cls, data: dict):
        return cls(
            type=data["type"],
            coordinates=data["coordinates"],
        )

    def is_polygon(self) -> bool:
        return self.type == "Polygon"

    def is_multipolygon(self) -> bool:
        return self.type == "MultiPolygon"


@dataclass(frozen=True)
class Point:
    lat: Decimal
    lon: Decimal

    def to_tuple(self):
        return (float(self.lat), float(self.lon))

    def to_geojson(self):
        return {
            "type": "Point",
            "coordinates": [float(self.lon), float(self.lat)],
        }

    @classmethod
    def from_geojson(cls, data: dict):
        if data.get("type") != "Point":
            raise ValueError("Invalid GeoJSON type for Point")

        lon, lat = data["coordinates"]
        return cls(lat=Decimal(str(lat)), lon=Decimal(str(lon)))

    def distance_to(self, other: "Point") -> float:
        """
        Haversine distance in kilometers.
        """
        R = 6371.0

        lat1 = radians(float(self.lat))
        lon1 = radians(float(self.lon))
        lat2 = radians(float(other.lat))
        lon2 = radians(float(other.lon))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c


class PointField(models.Field):
    description = "Geographic point (latitude, longitude)"

    def db_type(self, connection):
        # No se usa directamente
        return None

    def contribute_to_class(self, cls, name, private_only=False):
        self.lat_field = models.DecimalField(
            max_digits=9,
            decimal_places=6,
            null=self.null,
            blank=self.blank,
        )
        self.lon_field = models.DecimalField(
            max_digits=9,
            decimal_places=6,
            null=self.null,
            blank=self.blank,
        )

        cls.add_to_class(f"{name}_lat", self.lat_field)
        cls.add_to_class(f"{name}_lon", self.lon_field)

        super().contribute_to_class(cls, name)
