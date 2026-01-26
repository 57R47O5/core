
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";

export const TipoDocumentoIdentidadSchema = Yup.object().shape({
  nombre: Yup.mixed().nullable(),  descripcion: Yup.mixed().nullable(),
});

export function TipoDocumentoIdentidadFormFields() {

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
          
    </>
  );
}

export default function TipoDocumentoIdentidadForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={TipoDocumentoIdentidadSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
          <TipoDocumentoIdentidadFormFields/>
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
