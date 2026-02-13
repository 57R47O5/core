from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from framework.permisos import require_perm

class BaseOptionsAPIView(APIView):
    """
    Clase genérica para devolver opciones de un modelo.
    field → str o lista[str]
    Si algún field tiene choices → devuelve choices.
    Si no tiene choices:
        - si ?q= → filtra con OR entre todos los fields.
    """
    model = None
    field = None             # str | list[str]
    id_field = "id"
    desc_field = None
    order_by = None
    filtro = None
    url = ""
    view_permission = []

    def _get_fields(self):
        """Normaliza: devuelve una lista siempre."""
        if self.field is None:
            return []
        if isinstance(self.field, (list, tuple)):
            return list(self.field)
        return [self.field]

    def _get_model_field(self, name):
        """Devuelve el campo Django del modelo."""
        return self.model._meta.get_field(name)

    @require_perm(view_permission)
    def get_queryset(self):
        assert self.model is not None, (
            f"{self.__class__.__name__} debe definir 'model'"
        )

        qs = self.model.objects.all()

        # Filtros predefinidos
        if self.filtro and isinstance(self.filtro, dict):
            filtros_limpios = {
                k: v for k, v in self.filtro.items()
                if v not in (None, "")
            }
            if filtros_limpios:
                qs = qs.filter(**filtros_limpios)

        # Buscar mientras se escribe (?q=)
        q = self.request.query_params.get("q", "").strip()
        fields = self._get_fields()

        if q and fields:
            # Armar OR dinámico entre los fields que NO tienen choices
            q_obj = Q()

            for f in fields:
                model_field = self._get_model_field(f)

                # si tiene choices → no se usa para búsqueda
                if model_field.choices:
                    continue

                q_obj |= Q(**{f"{f}__icontains": q})

            qs = qs.filter(q_obj) if q_obj else qs.none()

        if self.order_by:
            qs = qs.order_by(self.order_by)

        return qs

    def get_id(self, obj):
        return getattr(obj, self.id_field)

    def get_desc(self, obj):
        return getattr(obj, self.desc_field) if self.desc_field else str(obj)

    @require_perm(view_permission)
    def get(self, request):

        fields = self._get_fields()

        # Caso: algún field tiene choices
        choice_fields = []
        for f in fields:
            model_field = self._get_model_field(f)
            if model_field.choices:
                choice_fields.append(model_field)

        if choice_fields:
            # Combinar todos los choices (evita duplicados)
            data = []
            agregados = set()

            for mf in choice_fields:
                for value, label in mf.choices:
                    if value not in agregados:
                        agregados.add(value)
                        data.append({"id": value, "descripcion": label})

            return Response(data)

        # Caso normal: queryset
        data = [
            {
                "id": self.get_id(obj),
                "descripcion": self.get_desc(obj)
            }
            for obj in self.get_queryset()
        ]
        return Response(data)

    @classmethod
    def route(cls):
        return f"{cls.url}/options/"

    @classmethod
    def name(cls):
        return f"{cls.url}-options/"   
