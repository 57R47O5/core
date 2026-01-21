"""
Project URL configuration.

Delegates routing to ORCO-managed apps.
"""
from config.urls.base import urlpatterns 
from django.urls import path, include

# urlpatterns = [
#     path("api/", include(urlpatterns)),
# ]