
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { documentoIdentidadFields } from "./DocumentoIdentidadFields";
import { useModelForm } from "../../../hooks/useModelForm";


export default function DocumentoIdentidadForm({
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  
  const {
    initialValues,
    validationSchema,
    columns,
    FormFields,
  } = useModelForm(documentoIdentidadFields);
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
    >
      <Form>
        <FormFields fields={documentoIdentidadFields} />
        <div className="text-end mt-3">
          <Button type="submit" disabled={submitting}>
            {submitting ? "Guardando..." : submitText}
          </Button>
        </div>
      </Form>
    </Formik>
  );
}