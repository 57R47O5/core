import { useNavigate } from "react-router-dom";
import { Spinner, Card, Form } from "react-bootstrap";
import { Formik } from "formik";
import CenteredCard from "../displays/CenteredCard";
import { useRouteMode } from "../../hooks/useRouteMode";
import {
  InstanceProvider,
  useInstance,
} from "../../context/InstanceContext";
import getAPIBase from "../../api/BaseAPI";
import Botonera from "../botonera/botonera";

function BaseFormPageContent({
  controller,
  FormComponent,
  redirectTo,
  titleNew,
  titleEdit,
}) {
  const { id, isCreate } = useRouteMode();
  const navigate = useNavigate();
  const { instance, loading } = useInstance();

  const { crear, editar, eliminar } = getAPIBase(controller);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (isCreate) {
        await crear(values);
        alert("Registro creado");
      } else {
        await editar(id, values);
        alert("Registro actualizado");
      }
      navigate(redirectTo);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    await eliminar(id);
    alert("Registro eliminado");
    navigate(redirectTo);
  };

  return (
    <CenteredCard>
      <Card.Body>
        <h3 className="mb-4 justify-content-center" style={{textAlign:"center"}}>
          {isCreate ? titleNew : titleEdit}
        </h3>

        <Formik
          enableReinitialize
          initialValues={instance}
          validationSchema={FormComponent.validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <FormComponent />

              <div className="d-flex justify-content-between mt-3">
                <Botonera
                  showSubmit={isCreate || instance?.capabilities?.editar}
                  submitLabel={isCreate ? "Crear" : "Actualizar"}
                  showDelete={instance?.capabilities?.eliminar}
                  onDelete={handleDelete}
                  onCancel={() => navigate(redirectTo)}
                  isSubmitting={isSubmitting}
                />
              </div>
            </Form>
          )}
        </Formik>
      </Card.Body>
    </CenteredCard>
  );
}

export default function BaseFormPage({
  controller,
  FormComponent,
  redirectTo = `/${controller}`,
  titleNew = "Nuevo Registro",
  titleEdit = "Editar Registro",
}) {
  const { id, isEdit } = useRouteMode();

  const defaults =
    FormComponent.initialValuesDefault || {};

  return (
    <InstanceProvider
      controller={controller}
      id={isEdit && id}
      defaults={defaults}
    >
      <BaseFormPageContent
        controller={controller}
        FormComponent={FormComponent}
        redirectTo={redirectTo}
        titleNew={titleNew}
        titleEdit={titleEdit}
      />
    </InstanceProvider>
  );
}