"""
Project URL configuration.

Delegates routing to ORCO-managed apps.
"""

from django.urls import path, include

urlpatterns = [
    path("api/", include("config.urls")),
]
