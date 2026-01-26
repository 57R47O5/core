
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";


export const PersonaSchema = Yup.object().shape({

});

export function PersonaFormFields() {

  return (
    <>
    
    </>
  );
}

export default function PersonaForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PersonaSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
          <PersonaFormFields/>
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
