import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useModelForm } from "../../../hooks/useModelForm";
import { personaFisicaFields } from "./PersonaFisicaFields";

export default function PersonaFisicaForm({
  initialValues: externalInitialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  const { isCreate } = useRouteMode();

  const {
    initialValues,
    validationSchema,
    FormFields,
  } = useModelForm(
    personaFisicaFields
  );

  return (
    <Formik
      enableReinitialize
      initialValues={externalInitialValues ?? initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
    >
      {() => (
        <Form>
          <FormFields />

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
