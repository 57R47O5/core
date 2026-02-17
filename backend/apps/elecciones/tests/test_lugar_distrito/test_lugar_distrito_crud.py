import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.elecciones.models.lugar_distrito import LugarDistrito


class TestLugarDistritoCRUD(APITestCase):

    def setUp(self):
        self.list_url = reverse('elecciones:lugar-distrito-list')
        self.payload = {
            "name": "Test LugarDistrito"
        }

    def test_create(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert LugarDistrito.objects.count() == 1

    def test_list(self):
        LugarDistrito.objects.create(name="Item 1")
        LugarDistrito.objects.create(name="Item 2")

        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_update(self):
        instance = LugarDistrito.objects.create(name="Old Name")

        detail_url = reverse(
            'elecciones:lugar-distrito-detail',
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
        instance = LugarDistrito.objects.create(name="To delete")

        detail_url = reverse(
            'elecciones:lugar-distrito-detail',
            args=[instance.id]
        )

        response = self.client.delete(detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert LugarDistrito.objects.count() == 0