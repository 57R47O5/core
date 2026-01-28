import pytest

@pytest.mark.django_db()
def test_inicial(auth_client):
    assert True
