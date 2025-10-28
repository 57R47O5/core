import json
import traceback
from functools import wraps
from os.path import split

from django.http import JsonResponse
from rest_framework import status


class ExcepcionBase(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.callstack = []

    def __str__(self):
        return self.mensaje

    def serialize(self):
        self.actualizar_callstack()
        return json.dumps({"mensaje": self.mensaje, "callstack": self.callstack})

    def actualizar_callstack(self):
        stack_summary = traceback.extract_tb(self.__traceback__)

        self.callstack = [
            {
                "filename": split(frame_summary.filename)[1],
                "name": frame_summary.name,
                "line": frame_summary.line,
                "lineno": frame_summary.lineno,
            }
            for frame_summary in stack_summary
        ]


class ExcepcionValidacion(ExcepcionBase):
    '''
    Excepciones lanzadas durante la validacion
    '''
    def __init__(self, mensaje, *args, **kwargs):
        super().__init__(mensaje, *args, **kwargs)

class ExcepcionPermisos(ExcepcionBase):
    '''
    Excepciones lanzadas por falta de permisos para realizar la acción
    '''
    def __init__(self, mensaje, *args, **kwargs):
        super().__init__(mensaje, *args, **kwargs)


def excepcion(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ExcepcionBase as e:
            response_data = e.serialize()
            return JsonResponse(
                json.loads(response_data), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return _wrapped_view