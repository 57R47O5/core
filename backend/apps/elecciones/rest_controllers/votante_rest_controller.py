from datetime import datetime
from typing import Dict, Any
from pandas import DataFrame
from django.db import transaction
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from framework.constantes.mensajes_error import MensajesError
from framework.permisos import PermisoGroup, P
from framework.models.basemodels import Constant
from framework.utils import leer_archivo

from apps.base.models.documento_identidad import DocumentoIdentidad, TipoDocumentoIdentidad
from apps.base.models.contacto import Contacto, TipoContacto
from apps.elecciones.models.votante import Votante
from apps.elecciones.serializers.votante_serializer import (
    VotanteCreateSerializer,
    VotanteUpdateSerializer,
    VotanteRetrieveSerializer)
from controllers.base.base_rest_controller import ModelRestController, require_permission, CapabilitySet, Capability
from apps.elecciones.services.votantes_service import CargaMasivaService

class PermisosVotante(PermisoGroup):
    VIEW=Constant("elecciones.votante.view")
    CREATE=Constant("elecciones.votante.create")
    UPDATE=Constant("elecciones.votante.update")
    DESTROY=Constant("elecciones.votante.destroy")


class VotanteRestController(ModelRestController):
    label = "Votante"
    model = Votante
    url = "votante"
    create_serializer = VotanteCreateSerializer
    update_serializer = VotanteUpdateSerializer
    retrieve_serializer = VotanteRetrieveSerializer    
    permisos = PermisosVotante

    capabilities = CapabilitySet(
        Capability(
            name="crear",
            permission=P(PermisosVotante.CREATE),
        ))
    
    def _get_filter(self, params):
        filtro = Q()
        for key, value in params.items():
            if key in  ['nombres', 'apellidos']:
                filtro &= Q(**{f"persona__{key}__icontains":value})
        return filtro

    def serialize_list(self, queryset):
        return list(queryset.values()
                    .annotate(
                        nombres=F("persona__nombres"),
                        apellidos=F("persona__apellidos"),
                        distrito=F("distrito__nombre"),
                    ).annotate(
                        descripcion=Concat(
                        F("nombres"),
                        Value(" "),
                        F("apellidos"),
                        )
                    ).values())
    
    @require_permission(PermisosVotante.CREATE)
    @action(detail=False, methods=["post"], url_path="carga-masiva")
    def carga_masiva(self, request):
        file=request.data.get("documento")
        file.seek(0)
        with transaction.atomic():
            dataframe = leer_archivo(file)
            datos_creacion = Formateador.formatear_dataframe(dataframe)
            self.crear_votantes(datos_creacion)

        return Response({"Carga masiva exitosa"}, status=status.HTTP_201_CREATED)

    def crear_votantes(self, datos:list[dict]):
        for dato in datos:
            serializer = VotanteCreateSerializer(data=dato)
            serializer.is_valid(raise_exception=True)
            votante=serializer.save()
            documento=dato.get("documento")
            if documento:
                documento_identidad = DocumentoIdentidad.objects.create(
                    persona=votante.persona.persona,
                    tipo=TipoDocumentoIdentidad.objects.CEDULA,
                    numero=documento)
            direccion=dato.get("direccion")
            if direccion:
                contacto = Contacto.objects.create(
                    persona=votante.persona.persona,
                    tipo=TipoContacto.objects.DIRECCION,
                    valor=direccion
                )
        return True

class Formateador:

    class Error(MensajesError):
        FORMATO_FECHA_INVALIDO = "El formato de fecha debe ser DD/MM/YYYY"

    MAPEO_CAMPOS = {
        "nombre": "nombres",
        "apellido": "apellidos",
        "numero_ced": "documento",
        "cod_dist": "distrito",
        "direccion": "direccion",
        "fecha_naci": "fecha_nacimiento",
    }


    @classmethod
    def limpiar_dataframe(cls, df: DataFrame) -> DataFrame:
        """Reemplaza valores nulos por cadenas vacías."""
        return df.fillna("")

    @staticmethod
    def convertir_fecha(valor: str) -> str:
        """Convierte fecha de DD/MM/YYYY a YYYY-MM-DD."""
        try:
            return datetime.strptime(valor, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(Formateador.Error.FORMATO_FECHA_INVALIDO)


    @classmethod
    def formatear_fila(cls, row: Dict[str, Any]) -> Dict[str, str]:
        """Convierte una fila en el diccionario esperado por el serializer."""
        resultado = {}
        for origen, destino in cls.MAPEO_CAMPOS.items():
            valor = row[origen]
            if origen == "fecha_naci":
                valor = cls.convertir_fecha(valor)
            resultado[destino] = valor
        return resultado

    @classmethod
    def formatear_dataframe(cls, df: DataFrame) -> list[Dict[str, str]]:
        df = cls.limpiar_dataframe(df)
        return [cls.formatear_fila(row) for _, row in df.iterrows()]
