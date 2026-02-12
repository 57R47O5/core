from django.conf import settings
from django.conf.urls.static import static
from apps.geo.urls.rest_urls import urlpatterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)