import json
from django.contrib.gis.geos import GEOSGeometry, Point
from django.db.transaction import atomic

from rest_framework import serializers
from apps.geo.models import Lugar, GeoNivel

class LugarSerializer(serializers.ModelSerializer):
    nivel = serializers.SlugRelatedField(
        slug_field="code",
        queryset=GeoNivel.objects.all()
    )

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
            "created_at",
            "updated_at",
        ]

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

    geom = serializers.JSONField()

    @atomic
    def create(self, validated_data):
        geom_json = validated_data.pop("geom")

        geom = GEOSGeometry(
            json.dumps(geom_json),
            srid=4326
        )

        centroide = geom.centroid

        instancia = Lugar.objects.create(
            geom=geom,
            centroide=centroide,
            **validated_data
        )

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
    geom = serializers.SerializerMethodField()
    centroide = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = LugarSerializer.Meta.fields + [
            "geom",
            "centroide",
        ]

    def get_geom(self, obj:Lugar):
        return json.loads(obj.geom.geojson) if obj.geom else None

    def get_centroide(self, obj:Lugar):
        return json.loads(obj.centroide.geojson) if obj.centroide else None

class PuntoInputSerializer(LugarInputSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

    @atomic
    def create(self, validated_data):
        lat = validated_data.pop("lat")
        lon = validated_data.pop("lon")

        point = Point(lon, lat, srid=4326)

        validated_data["geom"] = point
        validated_data["nivel"] = GeoNivel.objects.get(code="PUNTO")

        instancia = Lugar.objects.create(
            geom=point,
            centroide=point,
            **validated_data
        )

        return instancia
