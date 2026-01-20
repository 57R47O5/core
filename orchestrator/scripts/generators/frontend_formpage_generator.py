from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR

def generate_form_page(definition:DomainModelDefinition):
    """
    model_name llega en PascalCase, ejemplo: "Paciente" o "StockFactura".
    """
    model_name = definition.model_name
    app_name = definition.app_name

    kebab = model_name.replace("_", "-")      # stock-factura
    pascal = definition.ModelName             # StockFactura
    form_component = f"{pascal}Form"          # StockFacturaForm

    output_path = FRONTEND_DIR / "src" / "apps" / app_name / model_name / f"{pascal}FormPage.jsx"
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
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Archivo  generado en {output_path}")

    return True
