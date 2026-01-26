
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const PersonaFisicaSchema = Yup.object().shape({
  nombres: Yup.mixed().nullable(),
  apellidos: Yup.mixed().nullable(),
  fecha_nacimiento: Yup.mixed().nullable(),
});

export function PersonaFisicaFormFields({ prefix = "" }) {
 
  return (
    <>               

      <InputFormik
        name="nombres"
        label="Nombres"
      />          

      <InputFormik
        name="apellidos"
        label="Apellidos"
      />         

      <DatePickerFormik
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
      {(formik) => (
        <Form>
     <PersonaFisicaFormFields/>          
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
