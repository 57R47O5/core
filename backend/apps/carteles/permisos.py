from rest_framework.permissions import BasePermission
from apps.base.framework.permissions import user_has_role

class EsMedico(BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, "medico")

class EsAsistente(BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, "asistente")
