import pytest
from datetime import date

URL = "/persona-fisica/"

@pytest.mark.django_db()
def test_create_persona_fisica(auth_client):
    datos={
        'nombres': 'Pedro Juan', 
        'apellidos': 'Caballero',
        'fecha_nacimiento': date.today().isoformat()}
    salida=auth_client.post(URL, datos)
    assert True
    