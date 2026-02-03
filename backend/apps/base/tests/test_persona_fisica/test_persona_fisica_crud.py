import pytest
from datetime import date
from rest_framework import status
from apps.base.models.persona_fisica import PersonaFisica, Persona
from apps.base.models.tipo_documento_identidad import TipoDocumentoIdentidad
from apps.base.models.documento_identidad import DocumentoIdentidad

URL = "/persona-fisica/"
DATOS_CREACION={
    'nombres': 'Pedro Juan', 
    'apellidos': 'Caballero',
    'fecha_nacimiento': date.today().isoformat()
    }

def test_create_persona_fisica(auth_client):
    salida=auth_client.post(URL, DATOS_CREACION)
    assert salida.status_code == status.HTTP_201_CREATED
    assert  creacion_persona_fisica_exitosa(salida)
    instancia = PersonaFisica.objects.get(pk=salida.data["id"])
    return instancia

def test_delete_persona_fisica(auth_client):
    output_creacion=auth_client.post(URL, DATOS_CREACION)
    assert output_creacion.status_code == status.HTTP_201_CREATED
    instancia = PersonaFisica.objects.get(pk=output_creacion.data["id"])
    salida_delete=auth_client.delete(f"{URL}{instancia.pk}/" )
    assert salida_delete.status_code == status.HTTP_204_NO_CONTENT
    instancia.refresh_from_db()
    assert instancia.is_deleted
    assert instancia.persona.is_deleted

    
def creacion_persona_fisica_exitosa(salida):
    assert salida.data["nombres"] == DATOS_CREACION["nombres"]
    assert salida.data["apellidos"] == DATOS_CREACION["apellidos"]
    assert salida.data["fecha_nacimiento"] == DATOS_CREACION["fecha_nacimiento"]
    id = salida.data["id"]
    persona_id = salida.data["persona_id"]
    assert Persona.objects.filter(pk=persona_id).exists()
    assert PersonaFisica.objects.filter(pk=id).exists()
    return True