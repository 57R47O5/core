
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { useModelForm } from "../../../hooks/useModelForm";
import { SalidaFields } from "./SalidaFields";

export default function SalidaForm({
  initialValues: externalInitialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  const {
    initialValues,
    validationSchema,
    FormFields,
  } = useModelForm(
    SalidaFields
  );  

  return (
    <Formik
      enableReinitialize
      initialValues={externalInitialValues ?? initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
          <FormFields/>
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
