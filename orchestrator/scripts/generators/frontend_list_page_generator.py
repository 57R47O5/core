import os
import re


def to_kebab_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def generate_frontend_list_page(model_name, fields, base_path):
    model_kebab = to_kebab_case(model_name)
    model_folder = f"{base_path}/{model_kebab}"
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{model_name}ListPage.jsx"

    # Construimos las columnas en base a los fields del modelo
    columns_js = []
    for f in fields:
        name = f["name"]
        label = name.replace("_", " ").capitalize()
        columns_js.append(f'        {{ label: "{label}", field: "{name}" }},')

    columns_render = "\n".join(columns_js)

    content = f"""
import BaseListPage from "../../components/listados/BaseListPage";
import {model_name}Filter from "./{model_name}Filter";

export default function {model_name}ListPage() {{
  return (
    <BaseListPage
      controller="{model_kebab}"
      title="{model_name}"
      FilterComponent={model_name}Filter}}
      columns={[
{columns_render}
      ]}
    />
  );
}}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ ListPage generado:", file_path)


