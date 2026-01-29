from apps.base.urls.moneda_urls import urlpatterns as moneda_urls
from apps.base.urls.persona_urls import urlpatterns as persona_urls
from apps.base.urls.persona_fisica_urls import urlpatterns as persona_fisica_urls
from apps.base.urls.persona_juridica_urls import urlpatterns as persona_juridica_urls
from apps.base.urls.tipo_documento_identidad_urls import urlpatterns as tipo_doc_urls
from apps.base.urls.documento_identidad_urls import urlpatterns as documento_urls

urlpatterns = (
    moneda_urls
    + persona_urls
    + persona_fisica_urls
    + persona_juridica_urls
    + tipo_doc_urls
    + documento_urls
)
