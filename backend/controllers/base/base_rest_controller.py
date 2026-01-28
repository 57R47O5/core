from typing import Type

from django.db import models
from django.db.models import Q

from rest_framework import status, viewsets, serializers
from rest_framework.response import Response

from framework.exceptions import excepcion, ExcepcionValidacion

class BaseRestController(viewsets.ViewSet):
    pass

class ModelRestController(BaseRestController):
    model: Type[models.Model] = None
    create_serializer: Type[serializers.ModelSerializer] = None
    update_serializer: Type[serializers.ModelSerializer] = None
    retrieve_serializer: Type[serializers.ModelSerializer] = None

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values())

    @excepcion
    def list(self, request):
        LIMITE=100
        filtro=self._get_filter(request.query_params)
        queryset=self.model.objects.filter(filtro)
        lista=self.serialize_list(queryset)[:LIMITE]
        return Response(lista, status=status.HTTP_200_OK)

    def _get_filter(self, params):
        filtro = Q()
        model_fields = {f.name for f in self.model._meta.get_fields()}

        for key, value in params.items():
            # Si viene un lookup (ej: nombre__icontains) tomamos solo la parte antes del __
            field_name = key.split("__")[0]

            # Validamos que el campo base exista en el modelo
            if field_name in model_fields:
                try:
                    filtro &= Q(**{key: value})
                except Exception:
                    # Si el lookup no es válido ignoramos ese filtro
                    pass

        return filtro
    
    def _get_queryset(self, filtro):
        return self.model.objects.filter(filtro)

    @excepcion
    def create(self, request):
        serializer=self.create_serializer(data=request.data)
        if not serializer.is_valid():
            raise ExcepcionValidacion(str(serializer.errors))
        instancia=serializer.save()
        retrieve_serializer = self.retrieve_serializer(instancia)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

    @excepcion
    def retrieve(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        serializer=self.retrieve_serializer(instancia)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @excepcion
    def update(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        serializer=self.update_serializer(instancia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @excepcion
    def partial_update(self, request, pk=None):
        instancia = self.model.objects.get(pk=pk)
        serializer = self.update_serializer(
            instancia, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @excepcion
    def destroy(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        instancia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


