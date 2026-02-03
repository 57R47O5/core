import os
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR
from orchestrator.scripts.utils.naming import to_snake_case

# ============================================================
#  GENERADOR DEL FORM 
# ============================================================
def generate_frontend_form(definition:DomainModelDefinition):
    model_folder = FRONTEND_DIR / "src" / "apps" / definition.app_name / definition.model_name
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{definition.ModelName}Form.jsx"

    content = f"""
import {{ Formik, Form }} from "formik";
import {{ Button }} from "react-bootstrap";
import {{ useModelForm }} from "../../../hooks/useModelForm";
import {{ {definition.ModelName}Fields }} from "./{definition.ModelName}Fields";

export default function {definition.ModelName}Form({{
  initialValues: externalInitialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}}) {{
  const {{
    initialValues,
    validationSchema,
    FormFields,
  }} = useModelForm(
    {definition.ModelName}Fields
  );  

  return (
    <Formik
      enableReinitialize
      initialValues={{externalInitialValues ?? initialValues}}
      validationSchema={{validationSchema}}
      onSubmit={{onSubmit}}
    >
      {{(formik) => (
        <Form>
          <FormFields/>
          <div className="text-end mt-3">
            <Button type="submit" disabled={{submitting}}>
              {{submitting ? "Guardando..." : submitText}}
            </Button>
          </div>

        </Form>
      )}}
    </Formik>
  );
}} 
"""

    with open(file_path, "w", encoding="utf-8") as field:
        field.write(content)

    print("✅ Form generado:", file_path)


# ============================================================
#  GENERADOR DEL FILTER
# ============================================================

def generate_frontend_filter(definition:DomainModelDefinition):
    model_folder = FRONTEND_DIR / "src" / "apps" / definition.app_name / definition.model_name
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{definition.ModelName}Filter.jsx"

    content = f"""
import {{ Formik, Form }} from "formik";
import {{ Button }} from "react-bootstrap";
import {{ useModelForm }} from "../../../hooks/useModelForm";
import {{ {definition.ModelName}Fields }} from "./{definition.ModelName}Fields";

const {definition.ModelName}Filter = ({{ onSearch, loading }}) => {{
  const {{ initialValuesFilter, FilterFields }} = useModelForm(
  {definition.ModelName}Fields)
  
  return (
    <>
      <h5 className="mb-3">Filtrar {(definition.model_name).replace('_', ' ')}</h5>

      <Formik
        initialValues={{initialValuesFilter}}
        onSubmit={{(values) => onSearch(values)}}
      >
        {{() => (
          <Form>
            <div className="row">
            <FilterFields/>
            </div>

            <div className="text-end">
              <Button type="submit" variant="primary" disabled={{loading}}>
                Buscar
              </Button>
            </div>
          </Form>
        )}}
      </Formik>
    </>
  );
}};

export default {definition.ModelName}Filter;
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Filter generado:", file_path)

FIELD_MAP = {
    "string": {
        "initial": '""',
        "yup": "Yup.string()",
        "component": "InputFormik",
    },
    "email": {
        "initial": '""',
        "yup": "Yup.string().email('Email inválido')",
        "component": "InputFormik",
    },
    "date": {
        "initial": "null",
        "yup": "Yup.date()",
        "component": "DatePickerFormik",
    },
    "datetime": {
        "initial": "null",
        "yup": "Yup.date()",
        "component": "DatePickerFormik",
        "mode": "datetime",
    },
    "boolean": {
        "initial": "false",
        "yup": "Yup.boolean()",
        "component": "CheckboxFormik",
    },
    "ForeignKey": {
        "initial": "null",
        "yup": "Yup.number()",
        "component": "SelectFormik",
    },
}

def generate_frontend_fields(definition: DomainModelDefinition):
    model_folder = (
        FRONTEND_DIR / "src" / "apps" / definition.app_name / definition.model_name
    )
    os.makedirs(model_folder, exist_ok=True)

    file_path = model_folder / f"{definition.ModelName}Fields.jsx"

    imports = []
    fields_js = []

    for field in definition.extra_fields:
        if not field.appears_in_form:
            continue

        config = FIELD_MAP.get(field.type, FIELD_MAP["string"])

        label = field.name.replace("_", " ").capitalize()
        initial = config["initial"]
        yup = config["yup"]

        # required vs nullable
        if not (field.blank or field.null):
            yup += '.required("Requerido")'
        else:
            yup += ".nullable()"

        component = config["component"]
        imports.append(component)

        # render
        render_props = ""
        if field.type == "datetime":
            render_props = ' mode="datetime"'

        field_block = f"""
  {field.name}: {{
    label: "{label}",
    initial: {initial},
    form: true, 
    filter: true,
    validation: {yup},
    render: (props) => <{component} {{...props}}{render_props} />,
  }},
"""
        fields_js.append(field_block)

    # imports
    import_lines = ['import * as Yup from "yup";']
    for comp in sorted(imports):
        if comp != "Yup":
            import_lines.append(
                f'import {comp} from "../../../components/forms/{comp}";'
            )

    content = f"""
{chr(10).join(import_lines)}

export const {definition.ModelName}Fields = {{
{''.join(fields_js)}
}};
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

    print("✅ Fields generados:", file_path)