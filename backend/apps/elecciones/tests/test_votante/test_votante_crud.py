import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.elecciones.models.votante import Votante


class TestVotanteCRUD(APITestCase):

    def setUp(self):
        self.list_url = reverse('elecciones:votante-list')
        self.payload = {
            "name": "Test Votante"
        }

    def test_create(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Votante.objects.count() == 1

    def test_list(self):
        Votante.objects.create(name="Item 1")
        Votante.objects.create(name="Item 2")

        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_update(self):
        instance = Votante.objects.create(name="Old Name")

        detail_url = reverse(
            'elecciones:votante-detail',
            args=[instance.id]
        )

        response = self.client.put(
            detail_url,
            data=json.dumps({"name": "Updated Name"}),
            content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        instance.refresh_from_db()
        assert instance.name == "Updated Name"

    def test_delete(self):
        instance = Votante.objects.create(name="To delete")

        detail_url = reverse(
            'elecciones:votante-detail',
            args=[instance.id]
        )

        response = self.client.delete(detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Votante.objects.count() == 0