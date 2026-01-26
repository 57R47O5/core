
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";

export const MonedaSchema = Yup.object().shape({
  nombre: Yup.mixed().nullable(),  descripcion: Yup.mixed().nullable(),  simbolo: Yup.mixed().nullable(),
});

export function MonedaFormFields() {

  return (
    <>
    
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
      {(formik) => (
        <Form>
          <MonedaFormFields/>
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
