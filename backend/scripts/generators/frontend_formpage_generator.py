import re

def pascal_to_kebab(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()

def generate_form_page(model_name: str):
    """
    model_name llega en PascalCase, ejemplo: "Paciente" o "StockFactura".
    """
    kebab = pascal_to_kebab(model_name)       # stock-factura
    pascal = model_name                       # StockFactura
    form_component = f"{pascal}Form"          # StockFacturaForm

    return f'''import BaseFormPage from "../../components/forms/BaseFormPage";
import {form_component} from "./{form_component}";

export default function {pascal}FormPage() {{
  return (
    <BaseFormPage
      controller="{kebab}"
      FormComponent={ {form_component} }
      titleNew="Nuevo {pascal}"
      titleEdit="Editar {pascal}"
    />
  );
}}
'''
