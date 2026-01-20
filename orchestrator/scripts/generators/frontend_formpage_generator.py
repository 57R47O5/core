import re
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR


def generate_form_page(definition:DomainModelDefinition):
    """
    model_name llega en PascalCase, ejemplo: "Paciente" o "StockFactura".
    """
    model_name = definition.model_name
    app_name = definition.app_name

    kebab = model_name.replace("_", "-")       # stock-factura
    pascal = definition.ModelName                       # StockFactura
    form_component = f"{pascal}Form"          # StockFacturaForm

    output_file = FRONTEND_DIR / "src" / "apps" / app_name / model_name
    content = f'''import BaseFormPage from "../../components/forms/BaseFormPage";
import {form_component} from "./{form_component}";

export default function {pascal}FormPage() {{
  return (
    <BaseFormPage
      controller="{kebab}"
      FormComponent={{{form_component}}}
      titleNew="Nuevo {pascal}"
      titleEdit="Editar {pascal}"
    />
  );
}}
'''
    output_file.write_text(content, encoding="utf-8")

    print(f"Archivo  generado en {output_file}")

    return True
