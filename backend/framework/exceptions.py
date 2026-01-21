import json
import traceback
from functools import wraps
from os.path import split

from rest_framework import status
from rest_framework.response import Response


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

    def to_response(self):
        self.actualizar_callstack()
        return Response(
            {
                "mensaje": self.mensaje,
                "callstack": self.callstack,
            },
            status=self.http_status,
        )

class ExcepcionValidacion(ExcepcionBase):
    http_status = status.HTTP_400_BAD_REQUEST


class ExcepcionAutenticacion(ExcepcionBase):
    http_status = status.HTTP_401_UNAUTHORIZED


class ExcepcionPermisos(ExcepcionBase):
    http_status = status.HTTP_403_FORBIDDEN


def excepcion(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ExcepcionBase as e:
            return e.to_response()

    return _wrapped_view