
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";

export const MonedaSchema = Yup.object().shape({
  id: Yup.mixed().nullable(),  nombre: Yup.mixed().nullable(),  descripcion: Yup.mixed().nullable(),  simbolo: Yup.mixed().nullable(),
});

export function MonedaFormFields({ prefix = "" }) {
  const fieldName = (name) => prefix ? `${prefix}.${name}` : name;

  return (
    <>
    
      <InputFormik
        name="id"
        label="Id"
      />
          
      <InputFormik
        name="nombre"
        label="Nombre"
      />
          
      <InputFormik
        name="descripcion"
        label="Descripcion"
      />
          
      <InputFormik
        name="simbolo"
        label="Simbolo"
      />
          
    </>
  );
}

export default function MonedaForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={MonedaSchema}
      onSubmit={onSubmit}
    >
      {({ errors, touched }) => (
        <Form>

      <InputFormik
        name="id"
        label="Id"
      />
          
      <InputFormik
        name="nombre"
        label="Nombre"
      />
          
      <InputFormik
        name="descripcion"
        label="Descripcion"
      />
          
      <InputFormik
        name="simbolo"
        label="Simbolo"
      />
          
          <div className="text-end mt-3">
            <Button type="submit" disabled={submitting}>
              {submitting ? "Guardando..." : submitText}
            </Button>
          </div>

        </Form>
      )}
    </Formik>
  );
} 
