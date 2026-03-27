import { Spinner, Card, Form } from "react-bootstrap";
import { Formik } from "formik";
import CenteredCard from "../displays/CenteredCard";
import { useRouteMode } from "../../hooks/useRouteMode";
import { useInstance } from "../../context/InstanceContext";
import Botonera from "../botonera/botonera";
import { useFormSubmit } from "../../hooks/useFormSubmit";
import { useFormDelete } from "../../hooks/useFormDelete";
import { useBotoneraConfig } from "../../hooks/useBotoneraConfig";
import { resolveInitialValues } from "../../hooks/InitialValues";
import { resolveValidationSchema } from "../../hooks/ValidationSchema";

export default function BaseFormPage({FormComponent}) {
  const formModel = FormComponent();
  const { instance, loading, controller } = useInstance();
  const  { isCreate} = useRouteMode();
  const handleSubmit = useFormSubmit({controller});
  const handleDelete = useFormDelete({controller});
  const botoneraConfig = useBotoneraConfig({
    onDelete: handleDelete,
  });
  const context = instance?._context || {};

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
          {(formik) => {

            return (
              <Form>
                 <formModel.FormFields formik={formik} instance={instance} />
                <div className="d-flex justify-content-between mt-3">
                <Botonera
                  {...botoneraConfig}
                  isSubmitting={formik.isSubmitting}
                />
              </div>
              </Form>
            );
          }}
        </Formik>
      </Card.Body>
    </CenteredCard>
  );
}