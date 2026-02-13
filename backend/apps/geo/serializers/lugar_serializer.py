import json
from decimal import Decimal

from django.db.transaction import atomic
from rest_framework import serializers

from apps.geo.models import Lugar, GeoNivel
from apps.geo.framework.geometries import Geometry, Point


# =====================================================
# Base Output Serializer
# =====================================================

class LugarSerializer(serializers.ModelSerializer):
    nivel = serializers.SlugRelatedField(
        slug_field="code",
        queryset=GeoNivel.objects.all()
    )

    geometry = serializers.SerializerMethodField()
    centroide = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = [
            "id",
            "codigo",
            "nombre",
            "tipo",
            "descripcion",
            "nivel",
            "padre",
            "activo",
            "geometry",
            "centroide",
            "created_at",
            "updated_at",
        ]

    def get_geometry(self, obj: Lugar):
        return obj.geometry_data

    def get_centroide(self, obj: Lugar):
        if obj.centroide_lat is None or obj.centroide_lon is None:
            return None

        return {
            "lat": float(obj.centroide_lat),
            "lon": float(obj.centroide_lon),
        }

class LugarInputSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=255)
    tipo = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    nivel = serializers.SlugRelatedField(
        slug_field="code",
        queryset=GeoNivel.objects.all()
    )

    padre = serializers.PrimaryKeyRelatedField(
        queryset=Lugar.objects.all(),
        required=False,
        allow_null=True
    )

    geometry = serializers.JSONField(required=False, allow_null=True)

    @atomic
    def create(self, validated_data):
        geometry_json = validated_data.pop("geometry", None)

        instancia = Lugar.objects.create(**validated_data)

        # ------------------------------------------------
        # Asignar geometry usando propiedad de dominio
        # ------------------------------------------------
        if geometry_json:
            geometry = Geometry.from_geojson(geometry_json)
            instancia.geometry = geometry

            # calcular centroide desde dominio
            centroide = geometry.centroid()
            instancia.centroide = centroide

            instancia.save()

        return instancia

class LugarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = [
            "nombre",
            "descripcion",
            "activo",
        ]

class LugarRetrieveSerializer(LugarSerializer):
    pass

class PuntoInputSerializer(LugarInputSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

    @atomic
    def create(self, validated_data):
        lat = validated_data.pop("lat")
        lon = validated_data.pop("lon")

        validated_data.pop("geometry", None)

        nivel_punto = GeoNivel.objects.get(code="PUNTO")
        validated_data["nivel"] = nivel_punto

        instancia = Lugar.objects.create(**validated_data)

        point = Point(lat=lat, lon=lon)

        instancia.geometry = point
        instancia.centroide = point
        instancia.save()

        return instancia
