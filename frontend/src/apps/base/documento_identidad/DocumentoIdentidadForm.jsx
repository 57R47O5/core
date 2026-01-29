
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";


export const DocumentoIdentidadFields = {
  tipo: Yup.mixed().nullable(),
  numero: Yup.mixed().nullable(),
};

export function DocumentoIdentidadFormFields() {

  return (
    <>    
      <SelectFormik
        name="tipo"
        label="Tipo Documento"
        endpoint="tipo-documento-identidad"
      />
      <InputFormik
        name="numero"
        label="Numero de documento"
      />
                
    </>
  );
}

export default function DocumentoIdentidadForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={DocumentoIdentidadSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
          <DocumentoIdentidadFormFields/>
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
