import os

from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR


def generate_frontend_list_page(definition:DomainModelDefinition):
    model_kebab = (definition.model_name).replace("_","-")
    model_folder = model_folder = FRONTEND_DIR / "src" / "apps" / definition.app_name / definition.model_name
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{definition.ModelName}ListPage.jsx"

    # Construimos las columnas en base a los fields del modelo
    columns_js = []
    for field in definition.extra_fields:
      if not field.appears_in_form:
        continue
      name = field.name
      label = name.replace("_", " ").capitalize()
      columns_js.append(f'      {{ label: "{label}", field: "{name}" }}')

    columns_render = "{[\n" + ",\n".join(columns_js) + "\n      ]}"

    content = f"""
import BaseListPage from "../../../components/listados/BaseListPage";
import {definition.ModelName}Filter from "./{definition.ModelName}Filter";

export default function {definition.ModelName}ListPage() {{
  return (
    <BaseListPage
      controller="{model_kebab}"
      title="{definition.ModelName}"
      FilterComponent={{{definition.ModelName}Filter}}
      columns={columns_render}
    />
  );
  }}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ ListPage generado:", file_path)


