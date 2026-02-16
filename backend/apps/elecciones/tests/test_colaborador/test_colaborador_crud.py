import json
from datetime import date
from rest_framework import status
from apps.base.models.persona_fisica import PersonaFisica, Persona


URL = "/colaborador/"
DATOS_CREACION={
    'nombres': 'Pedro Juan', 
    'apellidos': 'Caballero',
    'fecha_nacimiento': date.today().isoformat()
    }

def test_create_colaborador(auth_client):
    salida=auth_client.post(URL, DATOS_CREACION)
    assert salida.status_code == status.HTTP_201_CREATED
    assert  creacion_persona_fisica_exitosa(salida)
    instancia = PersonaFisica.objects.get(pk=salida.data["id"])
    return instancia

def creacion_persona_fisica_exitosa(salida):
    assert salida.data["nombres"] == DATOS_CREACION["nombres"]
    assert salida.data["apellidos"] == DATOS_CREACION["apellidos"]
    assert salida.data["fecha_nacimiento"] == DATOS_CREACION["fecha_nacimiento"]
    id = salida.data["id"]
    persona_id = salida.data["persona_id"]
    assert Persona.objects.filter(pk=persona_id).exists()
    assert PersonaFisica.objects.filter(pk=id).exists()
    return True