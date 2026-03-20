
import { Formik, Form } from "formik";
import { Button, Spinner } from "react-bootstrap";
import { documentoIdentidadFields } from "./DocumentoIdentidadFields";
import { useModelForm } from "../../../hooks/useModelForm";
import { useInstance } from "../../../context/InstanceContext";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import O2MProvider from "../../../components/o2m/O2MProvider";


export function DocumentosPersona({}) {
  const { instance } = useInstance();

  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(documentoIdentidadFields);

  if (!instance)
    return (<Spinner/>)
  return (
    <O2MProvider
      controller="documento-identidad"
      columns={columns}
      initialItem={{
        ...initialValues,
        persona_id: instance.persona_id, 
      }}
      validationSchema={validationSchema}
    >
      <O2MInlineList        
        filtros={{persona_id: instance.persona_id }}
      />
    </O2MProvider>
  );
}

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