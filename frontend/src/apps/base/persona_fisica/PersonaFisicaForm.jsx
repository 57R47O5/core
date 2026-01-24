
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";

export const PersonaFisicaSchema = Yup.object().shape({
  persona: Yup.mixed().nullable(),  nombres: Yup.mixed().nullable(),  apellidos: Yup.mixed().nullable(),  fecha_nacimiento: Yup.mixed().nullable(),
});

export function PersonaFisicaFormFields({ prefix = "" }) {
  const fieldName = (name) => prefix ? `${prefix}.${name}` : name;

  return (
    <>
    
      <InputFormik
        name="persona"
        label="Persona"
      />
          
      <InputFormik
        name="nombres"
        label="Nombres"
      />
          
      <InputFormik
        name="apellidos"
        label="Apellidos"
      />
          
      <InputFormik
        name="fecha_nacimiento"
        label="Fecha nacimiento"
      />
          
    </>
  );
}

export default function PersonaFisicaForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PersonaFisicaSchema}
      onSubmit={onSubmit}
    >
      {({ errors, touched }) => (
        <Form>

      <InputFormik
        name="persona"
        label="Persona"
      />
          
      <InputFormik
        name="nombres"
        label="Nombres"
      />
          
      <InputFormik
        name="apellidos"
        label="Apellidos"
      />
          
      <InputFormik
        name="fecha_nacimiento"
        label="Fecha nacimiento"
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
