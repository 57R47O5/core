import json
from decimal import Decimal

from django.db import transaction

from apps.geo.models.lugar import Lugar
from apps.geo.models.geo_nivel import GeoNivel
from apps.elecciones.models.lugar_distrito import LugarDistrito
from apps.elecciones.models.distrito_electoral import DistritoElectoral


class DistritoGeoImportService:

    @classmethod
    def crear_distrito(cls, datos):
        return cls.import_geojson(json.load(datos))

    @classmethod
    @transaction.atomic
    def import_geojson(cls, geojson: dict):

        nivel = GeoNivel.objects.DISTRITO


        props = geojson["properties"]
        geometry = geojson["geometry"]

        nombre = props["DPTO_DESC"].strip()
        centroide_lat, centroide_lon = cls.compute_centroid(geometry)

        distrito = DistritoElectoral.objects.create(
            nombre=nombre,
            codigo=nombre,
            descripcion=nombre)

        lugar = Lugar.objects.create(
            geometry_data=geometry,
            tipo=geometry["type"],
            nivel=nivel,
            centroide_lat=centroide_lat,
            centroide_lon=centroide_lon
        )

        LugarDistrito.objects.create(
            distrito=distrito,
            lugar=lugar
        )
        return DistritoElectoral

    def compute_centroid(geometry):

        coords = []

        if geometry["type"] == "MultiPolygon":
            for polygon in geometry["coordinates"]:
                for ring in polygon:
                    coords.extend(ring)

        elif geometry["type"] == "Polygon":
            for ring in geometry["coordinates"]:
                coords.extend(ring)

        lon = sum(p[0] for p in coords) / len(coords)
        lat = sum(p[1] for p in coords) / len(coords)

        return Decimal(lat), Decimal(lon)