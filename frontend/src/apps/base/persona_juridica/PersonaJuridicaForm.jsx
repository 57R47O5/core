
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";

export const PersonaJuridicaSchema = Yup.object().shape({
  persona: Yup.mixed().nullable(),  razon_social: Yup.mixed().nullable(),  nombre_fantasia: Yup.mixed().nullable(),
});

export function PersonaJuridicaFormFields() {

  return (
    <>
    
      <InputFormik
        name="persona"
        label="Persona"
      />
          
      <InputFormik
        name="razon_social"
        label="Razon social"
      />
          
      <InputFormik
        name="nombre_fantasia"
        label="Nombre fantasia"
      />
          
    </>
  );
}

export default function PersonaJuridicaForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PersonaJuridicaSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
          <PersonaJuridicaFormFields/>
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
