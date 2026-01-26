import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.base.models.persona_user import PersonaUser


class TestPersonaUserCRUD(APITestCase):

    def setUp(self):
        self.list_url = reverse('base:persona-user-list')
        self.payload = {
            "name": "Test PersonaUser"
        }

    def test_create(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert PersonaUser.objects.count() == 1

    def test_list(self):
        PersonaUser.objects.create(name="Item 1")
        PersonaUser.objects.create(name="Item 2")

        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_update(self):
        instance = PersonaUser.objects.create(name="Old Name")

        detail_url = reverse(
            'base:persona-user-detail',
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
        instance = PersonaUser.objects.create(name="To delete")

        detail_url = reverse(
            'base:persona-user-detail',
            args=[instance.id]
        )

        response = self.client.delete(detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PersonaUser.objects.count() == 0