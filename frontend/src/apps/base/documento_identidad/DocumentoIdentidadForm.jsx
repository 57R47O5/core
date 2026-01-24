
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const DocumentoIdentidadSchema = Yup.object().shape({
  persona: Yup.mixed().nullable(),  tipo: Yup.mixed().nullable(),  numero: Yup.mixed().nullable(),  pais_emision: Yup.mixed().nullable(),  vigente: Yup.mixed().nullable(),
});

export function DocumentoIdentidadFormFields({ prefix = "" }) {
  const fieldName = (name) => prefix ? `${prefix}.${name}` : name;

  return (
    <>
    
      <SelectFormik
        name="persona"
        label="Persona"
        endpoint="persona"
      />
          
      <SelectFormik
        name="tipo"
        label="Tipo"
        endpoint="tipo-documento-identidad"
      />
          
      <InputFormik
        name="numero"
        label="Numero"
      />
          
      <InputFormik
        name="pais_emision"
        label="Pais emision"
      />
          
      <InputFormik
        name="vigente"
        label="Vigente"
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
      {({ errors, touched }) => (
        <Form>

      <SelectFormik
        name="persona"
        label="Persona"
        endpoint="persona"
      />
          
      <SelectFormik
        name="tipo"
        label="Tipo"
        endpoint="tipo-documento-identidad"
      />
          
      <InputFormik
        name="numero"
        label="Numero"
      />
          
      <InputFormik
        name="pais_emision"
        label="Pais emision"
      />
          
      <InputFormik
        name="vigente"
        label="Vigente"
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
