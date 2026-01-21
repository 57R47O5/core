"""
Base URL configuration.

Routes are provided by ORCO-managed apps.
"""

from django.urls import include, path
from config.settings.orc_apps import ORC_APPS

urlpatterns = []

for app in ORC_APPS:
    try:
        urlpatterns.append(
            path("", include(f"{app}.urls"))
        )    
    except ModuleNotFoundError:
        pass