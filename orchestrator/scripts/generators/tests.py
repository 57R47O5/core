import os
from orchestrator.scripts.generators.paths import APPS_DIR
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition

def generate_model_tests(definition:DomainModelDefinition):
    """
    Genera tests CRUD básicos para un modelo.
    Se ejecuta como parte de: orc generate <model> <app>
    """

    model_name = definition.model_name
    ModelName = definition.ModelName
    app_name = definition.app_name
    model_kebab = model_name.replace("_", "-")


    tests_dir = (
        APPS_DIR
        / app_name
        / "tests"
        / f"test_{model_name}"
    )

    os.makedirs(tests_dir, exist_ok=True)

    # __init__.py
    init_file = tests_dir / "__init__.py"
    init_file.touch(exist_ok=True)

    test_file = tests_dir / f"test_{model_name}_crud.py"

    content = f"""
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.{app_name}.models import {ModelName}


class Test{ModelName}CRUD(APITestCase):

    def setUp(self):
        self.list_url = reverse('{app_name}:{model_kebab}-list')
        self.payload = {{
            "name": "Test {ModelName}"
        }}

    def test_create(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.payload),
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert {ModelName}.objects.count() == 1

    def test_list(self):
        {ModelName}.objects.create(name="Item 1")
        {ModelName}.objects.create(name="Item 2")

        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_update(self):
        instance = {ModelName}.objects.create(name="Old Name")

        detail_url = reverse(
            '{app_name}:{model_kebab}-detail',
            args=[instance.id]
        )

        response = self.client.put(
            detail_url,
            data=json.dumps({{"name": "Updated Name"}}),
            content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        instance.refresh_from_db()
        assert instance.name == "Updated Name"

    def test_delete(self):
        instance = {ModelName}.objects.create(name="To delete")

        detail_url = reverse(
            '{app_name}:{model_kebab}-detail',
            args=[instance.id]
        )

        response = self.client.delete(detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert {ModelName}.objects.count() == 0
""".strip()

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🧪 Tests CRUD generados: {test_file}")
