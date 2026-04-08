import { Spinner, Card, Form } from "react-bootstrap";
import { Formik } from "formik";
import CenteredCard from "../displays/CenteredCard";
import { useInstance } from "../../context/InstanceContext";
import Botonera from "../botonera/Botonera";
import { useFormSubmit } from "../../hooks/useFormSubmit";
import { useFormDelete } from "../../hooks/useFormDelete";
import { useBotoneraConfig } from "../../hooks/useBotoneraConfig";
import { resolveInitialValues } from "../../hooks/InitialValues";
import { resolveValidationSchema } from "../../hooks/ValidationSchema";

export default function BaseFormPage({ FormComponent }) {
  const { id, instance, exists, loading, controller } = useInstance();

  return (
    <BaseFormPageInner
      FormComponent={FormComponent}
      id={id}
      instance={instance}
      exists={exists}
      loading={loading}
      controller={controller}
    />
  );
}

export function BaseFormPageInner({
  FormComponent,
  id,
  instance,
  exists,
  loading,
  controller,
}) {
  const formModel = FormComponent();

  const handleSubmit = useFormSubmit({ id, exists, controller });
  const handleDelete = useFormDelete({ id, controller });

  const botoneraConfig = useBotoneraConfig({
    onDelete: handleDelete,
  });

  const context = instance?._context || {};
  const isCreate = !exists;

  const initialValues = resolveInitialValues({
    formModel,
    context,
    FormComponent,
  });

  const validationSchema = resolveValidationSchema({
    formModel,
    FormComponent,
    context,
  });

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <CenteredCard>
      <Card.Body>
        <h3 className="mb-4 text-center">
          {isCreate ? "Nuevo Registro" : "Editar Registro"}
        </h3>

        <Formik
          enableReinitialize
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {(formik) => (
            <Form>
              <formModel.FormFields formik={formik} instance={instance} />

              <div className="d-flex justify-content-between mt-3">
                <Botonera
                  {...botoneraConfig}
                  isSubmitting={formik.isSubmitting}
                />
              </div>
            </Form>
          )}
        </Formik>
      </Card.Body>
    </CenteredCard>
  );
}