from typing import Type, List, Optional
from django.db import models
from django.db.models import Q, CharField, TextField, DateField, DateTimeField

from rest_framework import status, viewsets, serializers
from rest_framework.response import Response

from framework.menu.menu import Node
from framework.exceptions import excepcion, ExcepcionValidacion
from framework.permisos import Perm, require_perm

class BaseRestController(viewsets.ViewSet):
    label:str
    url:str
    permisos:Optional[List[str]]

    @classmethod
    def to_node(cls)->Node:
        '''
        Obtiene un nodo para el menu a partir del controller
        '''
        nodo_controller = Node(
            label=cls.label, 
            permiso=cls.permisos,
            to=f'/{cls.url}'
            )
        return nodo_controller
    
    def dispatch(self, request, *args, **kwargs):
        # 1. autenticación artesanal
        if not getattr(request, "user", None):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # 2. autorización por action
        perm = self._get_required_perm()
        if perm is not None:
            user_perms = request.user.permisos  # set[str]
            if not perm.evaluate(user_perms):
                return Response(status=status.HTTP_403_FORBIDDEN)

        return super().dispatch(request, *args, **kwargs)


class ModelRestController(BaseRestController):
    model: Type[models.Model] = None
    create_serializer: Type[serializers.ModelSerializer] = None
    update_serializer: Type[serializers.ModelSerializer] = None
    retrieve_serializer: Type[serializers.ModelSerializer] = None

    create_permission: Type[Perm] = None
    update_permission: Type[Perm] = None
    destroy_permission: Type[Perm] = None
    view_permission: Type[Perm] = None

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        return list(queryset.values())

    @require_perm(view_permission)
    def list(self, request):
        LIMITE=100
        filtro=self._get_filter(request.query_params)
        queryset=self.model.objects.filter(filtro)
        lista=self.serialize_list(queryset)[:LIMITE]
        return Response(lista, status=status.HTTP_200_OK)

    def _get_filter(self, params):
        filtro = Q()

        model_fields = {
            f.name: f
            for f in self.model._meta.get_fields()
            if hasattr(f, "get_internal_type")
        }

        for key, value in params.items():
            if value in (None, "", []):
                continue

            # nombre__lookup → nombre
            field_name, *lookup_parts = key.split("__")
            field = model_fields.get(field_name)

            if not field:
                continue

            try:
                # Si el frontend ya mandó lookup explícito → respetar
                if lookup_parts:
                    filtro &= Q(**{key: value})
                    continue

                # Inferir lookup por tipo de campo
                if isinstance(field, (CharField, TextField)):
                    filtro &= Q(**{f"{field_name}__icontains": value})

                elif isinstance(field, (DateField, DateTimeField)):
                    # igualdad por defecto (el FE puede mandar __gte/__lte)
                    filtro &= Q(**{field_name: value})

                else:
                    # Integer, FK, Boolean, UUID, etc
                    filtro &= Q(**{field_name: value})

            except Exception:
                # lookup inválido → ignorar
                pass

        return filtro
        
    def _get_queryset(self, filtro):
        return self.model.objects.filter(filtro)

    @excepcion
    @require_perm(create_permission)
    def create(self, request):
        serializer=self.create_serializer(data=request.data)
        if not serializer.is_valid():
            raise ExcepcionValidacion(str(serializer.errors))
        instancia=serializer.save()
        retrieve_serializer = self.retrieve_serializer(instancia)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

    @excepcion
    @require_perm(view_permission)
    def retrieve(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        serializer=self.retrieve_serializer(instancia)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @excepcion
    @require_perm(update_permission)
    def update(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        serializer=self.update_serializer(instancia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @excepcion
    @require_perm(update_permission)
    def partial_update(self, request, pk=None):
        instancia = self.model.objects.get(pk=pk)
        serializer = self.update_serializer(
            instancia, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @excepcion
    @require_perm(destroy_permission)
    def destroy(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        instancia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)