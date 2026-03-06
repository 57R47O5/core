from typing import Type, List, Optional, Callable
from django.db import models
from django.db.models import Q, CharField, TextField, DateField, DateTimeField

from rest_framework import status, viewsets, serializers
from rest_framework.response import Response

from framework.menu.menu import Node
from framework.exceptions import excepcion, ExcepcionValidacion, ExcepcionPermisos
from framework.permisos import Perm, require_perm, PermisoGroup, P

class Capability:
    """
    Representa una acción que puede realizarse sobre una instancia.
    Combina:
      - Permiso del usuario
      - Regla de negocio del modelo
    """

    def __init__(self, name, 
                 permission:Optional[Perm]=None, 
                 business_rule:Optional[str|Callable]=None):
        self.name = name
        self.permission = permission
        self.business_rule = business_rule

    def is_allowed(self, request, instance):
        allowed = True

        # Permiso
        if self.permission:
            allowed = allowed and self.permission.evaluate(request.user.permisos)

        # Regla de negocio
        if self.business_rule:
            if callable(self.business_rule):
                allowed &= self.business_rule(instance)
            else:
                rule = getattr(instance, self.business_rule, None)
                if callable(rule):
                    allowed &= rule()

        return allowed
    
class CapabilitySet:
    """
    Colección de capacidades evaluables.
    """

    def __init__(self, *capabilities):
        self._capabilities = list(capabilities)

    def evaluate(self, request, instance):
        return {
            cap.name: cap.is_allowed(request, instance)
            for cap in self._capabilities
        }

    def __iter__(self):
        return iter(self._capabilities)
    
    def __add__(self, other):
        if not isinstance(other, CapabilitySet):
            return NotImplemented

        # merge por nombre (el segundo sobrescribe)
        merged = {cap.name: cap for cap in self._capabilities}

        for cap in other:
            merged[cap.name] = cap

        return CapabilitySet(*merged.values())


from rest_framework.permissions import BasePermission


class ControllerPermission(BasePermission):

    def has_permission(self, request, view):
        acciones_rest = {'list':"view_permission",
                         "retrieve":"view_permission", 
                         "create":"create_permission",
                         "update":"update_permission",
                         "partial_update":"update_permission",
                         "destroy":"destroy_permission",}
        permiso_requerido = getattr(view, acciones_rest.get(view.action, ""), None)
        if permiso_requerido and not permiso_requerido.evaluate(request.user.permisos):
            raise ExcepcionPermisos("No tiene permisos para esta acción")

        return True   
class BaseRestController(viewsets.ViewSet):
    label:str
    url:str
    permisos: Type[PermisoGroup] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.permisos:

            constants = cls.permisos.constants()

            if "VIEW" in constants:
                cls.view_permission = P(constants["VIEW"])

            if "CREATE" in constants:
                cls.create_permission = P(constants["CREATE"])

            if "UPDATE" in constants:
                cls.update_permission = P(constants["UPDATE"])

            if "DESTROY" in constants:
                cls.destroy_permission = P(constants["DESTROY"])

    @classmethod
    def to_node(cls)->Node:
        '''
        Obtiene un nodo para el menu a partir del controller
        '''
        nodo_controller = Node(
            label=cls.label, 
            permiso=cls.permisos.to_perm(),
            to=f'/{cls.url}'
            )
        return nodo_controller

class ModelRestController(BaseRestController):
    model: Type[models.Model] = None
    create_serializer: Type[serializers.ModelSerializer] = None
    update_serializer: Type[serializers.ModelSerializer] = None
    retrieve_serializer: Type[serializers.ModelSerializer] = None
    permission_classes = [ControllerPermission]

    create_permission: Type[Perm] = None
    update_permission: Type[Perm] = None
    destroy_permission: Type[Perm] = None
    view_permission: Type[Perm] = None
   
    capabilities = CapabilitySet()

    def get_base_capabilities(self):

        caps = []

        if self.update_permission:
            caps.append(
                Capability(
                    name="editar",
                    permission=self.update_permission
                )
            )

        if self.destroy_permission:
            caps.append(
                Capability(
                    name="eliminar",
                    permission=self.destroy_permission
                )
            )

        return CapabilitySet(*caps)

    def get_capabilities(self):
        return self.get_base_capabilities() + self.capabilities

    def serialize_list(self, queryset):
        """
        Serialización rápida por defecto usando .values().
        Puede ser sobrescrita por subclases si requieren algo custom.
        """
        model = queryset.model
        if hasattr(model, "descripcion_expression") and \
            not hasattr(model, "descripcion"):
            queryset = queryset.annotate(
                descripcion=model.descripcion_expression()
            )

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
        return Response(self._serialize_instance(request, instancia), status=status.HTTP_201_CREATED)

    @excepcion
    @require_perm(view_permission)
    def retrieve(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        return Response(self._serialize_instance(request, instancia),
                         status=status.HTTP_200_OK)
    
    @excepcion
    @require_perm(update_permission)
    def update(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        serializer=self.update_serializer(instancia, data=request.data)
        serializer.is_valid(raise_exception=True)
        instancia=serializer.save()
        return Response(self._serialize_instance(request, instancia), status=status.HTTP_200_OK)

    @excepcion
    @require_perm(update_permission)
    def partial_update(self, request, pk=None):
        instancia = self.model.objects.get(pk=pk)
        serializer = self.update_serializer(
            instancia, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        instancia=serializer.save()
        return Response(self._serialize_instance(request, instancia), status=status.HTTP_200_OK)

    @excepcion
    @require_perm(destroy_permission)
    def destroy(self, request, pk=None):
        instancia=self.model.objects.get(pk=pk)
        instancia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    def _get_capabilities(self, request, instancia):
        '''
        Obtiene todas las operaciones que se pueden realizar con la instancia
        En esencia, combina Reglas del negocio con Permisos
        '''
        return self.get_capabilities().evaluate(request, instancia)


    def _serialize_instance(self, request, instancia):
        '''
        Método unificado para serializar todas las instancias.  
        Lo hacemos en dos partes. En primer lugar  serializamos 
        la instancia propiamente dicha y luego la enriquecemos.

        Esto nos permite mostrar no sólo lo que la instancia es,
        sino lo que se puede hacer con ella de acuerdo a los permisos
        que tenga el usuario
        '''
        serializer = self.retrieve_serializer(
            instancia,
            context={"request": request}
        )

        data = serializer.data

        capabilities = self._get_capabilities(request, instancia)

        if capabilities:
            data["capabilities"] = capabilities

        return data