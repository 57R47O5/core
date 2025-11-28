from apps.base.framework.exceptions import ExcepcionValidacion
from rest_framework.response import Response
from rest_framework.views import APIView

class BaseOptionsAPIView(APIView):
    """
    Clase genérica para devolver opciones de un modelo.
    """
    model = None
    field = None
    id_field = "id"
    desc_field = None           # por defecto usamos str(obj)
    order_by = None

    def get_queryset(self):
        assert self.model is not None, (
            f"{self.__class__.__name__} debe definir el atributo 'model'"
        )

        qs = self.model.objects.all()
        if self.order_by:
            qs = qs.order_by(self.order_by)
        return qs

    def get_id(self, obj):
        return getattr(obj, self.id_field)

    def get_desc(self, obj):
        if self.desc_field:
            return getattr(obj, self.desc_field)
        return str(obj)  

    def get(self, request):

        if self.field:
            field = self.model._meta.get_field(self.field)

            if not field.choices:
                raise ExcepcionValidacion(
                    f"El campo '{self.field}' no tiene choices definidos."
                )

            data = [
                {"id": value, "descripcion": label}
                for value, label in field.choices
            ]

        else:
            data = [
                {
                    "id": self.get_id(obj),
                    "descripcion": self.get_desc(obj)
                }
                for obj in self.get_queryset()
            ]
        return Response(data)
