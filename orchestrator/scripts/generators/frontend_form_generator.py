import os
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR
from orchestrator.utils.naming import to_snake_case

# ============================================================
#  GENERADOR DEL FORM 
# ============================================================
def generate_frontend_form(definition:DomainModelDefinition):
    model_folder = FRONTEND_DIR / "src" / "apps" / definition.app_name / definition.model_name
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{definition.ModelName}Form.jsx"

    imports = set()

    yup_entries = []
    form_fields_jsx = []
    embedded_forms = []
    embedded_schemas = []

    for field in definition.extra_fields:
        if not field.appears_in_form:
            continue
        required = None

        if field.is_foreign_key and field.is_embedded:
          ref_model = field.references_model
          ref_app = field.references_app

          imports.add(
              f"{{ {ref_model}FormFields, {ref_model}Schema }} "
              f'from "../../{ref_app}/{to_snake_case(ref_model)}/{ref_model}Form"'
          )

          embedded_schemas.append(
              f"  {field.name}: {ref_model}Schema,"
          )

          form_fields_jsx.append(f"""
          <{ref_model}FormFields prefix="{field.name}" />
          """)

          continue

        # YUP
        yup_line = f"{field.name}: "

        if field.type == "string":
            yup_line += "Yup.string()"
        elif field.type == "email":
            yup_line += "Yup.string().email('Email inválido')"
        elif field.type in ["date", "datetime"]:
            yup_line += "Yup.date()"
        elif field.type == "number":
            yup_line += "Yup.number()"
        elif field.type == "boolean":
            yup_line += "Yup.boolean()"
        else:
            yup_line += "Yup.mixed()"

        if required:
            yup_line += f".required('El campo {field.name} es obligatorio')"
        else:
            yup_line += ".nullable()"

        yup_entries.append("  " + yup_line + ",")
        schema_entries = yup_entries + embedded_schemas

        # COMPONENTES FRONT
        label = field.name.replace("_", " ").capitalize()

        if field.type in ("string", "email", "number"):
            imports.add("InputFormik")
            extra = ' type="email"' if field.type == "email" else ""
            jsx = f"""
        <InputFormik
          name="{field.name}"
          label="{label}"
          {extra}
        />
            """

        elif field.type == "boolean":
            imports.add("CheckboxFormik")
            jsx = f"""
        <CheckboxFormik
          name="{field.name}"
          label="{label}"
        />
            """

        elif field.type in ("date", "datetime"):
            imports.add("DatepickerFormik")
            mode = "datetime" if field.type == "datetime" else "date"
            jsx = f"""
        <DatepickerFormik
          name="{field.name}"
          label="{label}"
          mode="{mode}"
        />
            """

        elif field.type == "foreignkey":
            imports.add("SelectFormik")
            endpoint = to_snake_case(field.references_model).replace("_", "-")
            jsx = f"""
        <SelectFormik
          name="{field.name}"
          label="{label}"
          endpoint="{endpoint}"
        />
            """

        else:
            imports.add("InputFormik")
            jsx = f"""
        <InputFormik
          name="{field.name}"
          label="{label}"
        />
            """

        form_fields_jsx.append(jsx)

    imports_code = "\n".join(
        [f'import {imp} from "../../components/formik/{imp}";' for imp in sorted(imports)]
    )

    content = f"""
import {{ Formik, Form }} from "formik";
import * as Yup from "yup";
import {{ Button }} from "react-bootstrap";
{imports_code}

export const {definition.ModelName}Schema = Yup.object().shape({{
{os.linesep.join(schema_entries)}
}});

export function {definition.ModelName}FormFields({{ prefix = "" }}) {{
  const fieldName = (name) => prefix ? `${{prefix}}.${{name}}` : name;

  return (
    <>
    {os.linesep.join(form_fields_jsx)}
    </>
  );
}}

export default function {definition.ModelName}Form({{
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}}) {{
  return (
    <Formik
      enableReinitialize
      initialValues={{initialValues}}
      validationSchema={{{definition.ModelName}Schema}}
      onSubmit={{onSubmit}}
    >
      {{({{ errors, touched }}) => (
        <Form>
{os.linesep.join(form_fields_jsx)}
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
#  NUEVO: GENERADOR DEL FILTER
# ============================================================

def generate_frontend_filter(model_name, fields, base_path):
    model_kebab = (model_name).replace("_","-")
    model_folder = f"{base_path}/{model_kebab}"
    os.makedirs(model_folder, exist_ok=True)

    file_path = f"{model_folder}/{model_name}Filter.jsx"

    # Campos iniciales vacíos
    initial_values = []
    jsx_fields = []

    for f in fields:
        name = f["name"]
        ftype = f["type"]
        label = name.replace("_", " ").capitalize()
        initial_values.append(f"      {name}: \"\",")

        # Construcción del Field
        if ftype in ("string", "email", "number"):
            jsx = f"""
              <div className="col-md-3 mb-3">
                <RBForm.Label>{label}</RBForm.Label>
                <Field name="{name}" className="form-control" />
              </div>
            """

        elif ftype in ("date", "datetime"):
            input_type = "datetime-local" if ftype == "datetime" else "date"
            jsx = f"""
              <div className="col-md-3 mb-3">
                <RBForm.Label>{label}</RBForm.Label>
                <Field name="{name}" type="{input_type}" className="form-control" />
              </div>
            """

        elif ftype == "boolean":
            jsx = f"""
              <div className="col-md-2 mb-3 form-check">
                <Field name="{name}" type="checkbox" className="form-check-input" />
                <RBForm.Label className="form-check-label">{label}</RBForm.Label>
              </div>
            """

        elif ftype == "foreignkey":
            jsx = f"""
              <div className="col-md-3 mb-3">
                <RBForm.Label>{label}</RBForm.Label>
                <Field as="select" name="{name}" className="form-control">
                  <option value="">Seleccione...</option>
                </Field>
              </div>
            """

        else:
            jsx = f"""
              <div className="col-md-3 mb-3">
                <RBForm.Label>{label}</RBForm.Label>
                <Field name="{name}" className="form-control" />
              </div>
            """

        jsx_fields.append(jsx)

    content = f"""
import {{ Formik, Form, Field }} from "formik";
import {{ Button, Form as RBForm }} from "react-bootstrap";

const {model_name}Filter = ({{ onSearch, loading }}) => {{
  return (
    <>
      <h5 className="mb-3">Filtrar {(model_name).replace('_', ' ')}</h5>

      <Formik
        initialValues={{
{os.linesep.join(initial_values)}
        }}
        onSubmit={{(values) => onSearch(values)}}
      >
        {{() => (
          <Form>
            <div className="row">

{os.linesep.join(jsx_fields)}

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

export default {model_name}Filter;
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Filter generado:", file_path)

