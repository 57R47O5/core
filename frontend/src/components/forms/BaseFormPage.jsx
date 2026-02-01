import { useNavigate } from "react-router-dom";
import { Spinner, Card, Button } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import { useRouteMode } from "../../hooks/useRouteMode";
import { InstanceProvider, useInstance } from "../../context/InstanceContext";
import getAPIBase from "../../api/BaseAPI";

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

  const handleSubmit = async (values) => {
    if (isCreate) {
      await crear(values);
      alert("Registro creado");
    } else {
      await editar(id, values);
      alert("Registro actualizado");
    }
    navigate(redirectTo);
  };

  const handleDelete = async () => {
    await eliminar(id);
    alert("Registro eliminado");
    navigate(redirectTo);
  };

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
        <h3 className="mb-4">
          {isCreate ? titleNew : titleEdit}
        </h3>

        <FormComponent
          initialValues={instance}
          onSubmit={handleSubmit}
          submitText={isCreate ? "Crear" : "Actualizar"}
        />

        <div className="d-flex justify-content-between mt-3">
          <Button
            variant="secondary"
            onClick={() => navigate(redirectTo)}
          >
            Volver
          </Button>

          {!isCreate && (
            <Button
              variant="danger"
              onClick={handleDelete}
            >
              Eliminar
            </Button>
          )}
        </div>
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

