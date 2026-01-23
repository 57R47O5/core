import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Spinner, Card, Button } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import getAPIBase from "../../api/BaseAPI";
import { useRouteMode } from "../../hooks/useRouteMode";

/**
 * BaseFormPage
 * 
 * Props:
 * - controller: string (ej "pacientes")
 * - FormComponent: componente de Formik con props:
 *        - initialValuesDefault  (objeto requerido)
 *        - initialValues
 *        - onSubmit
 *        - submitting
 *        - submitText
 * 
 * - redirectTo: string (ruta donde volver después de crear/editar)
 */
export default function BaseFormPage({
  controller,
  FormComponent,
  redirectTo = `/${controller}`,
  titleNew = "Nuevo Registro",
  titleEdit = "Editar Registro",
}) {
  const { id, isCreate } = useRouteMode();
  const navigate = useNavigate();
  const { obtener, editar, crear } = getAPIBase(controller);

  // Tomamos los initialValues por defecto desde el form recibido
  const initialDefaults =
    FormComponent.initialValuesDefault || {};

  const [initialValues, setInitialValues] = useState(initialDefaults);
  const [cargando, setCargando] = useState(!!id);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const cargarInstancia = async () => {
      if (isCreate) {
      setInitialValues(initialDefaults);
      setCargando(false);
      return;
    }

    const data = await obtener(id);
    setInitialValues({ ...initialDefaults, ...data });
    setCargando(false);
    };
    if (id) cargarInstancia();
  }, [id]);

  const handleSubmit = async (values) => {
    try {
      setSubmitting(true);

      if (isCreate) {
        await crear(values);
        alert("Registro creado");
      } else {
        await editar(id, values);
        alert("Registro actualizado");
      }

      navigate(redirectTo);
    } catch (error) {
      console.error(error);
      alert("Error al guardar");
    } finally {
      setSubmitting(false);
    }
  };

  if (cargando) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <CenteredCard>
      <Card.Body>
        <h3 className="mb-4">{isCreate ? titleNew : titleEdit}</h3>

        <FormComponent
          initialValues={initialValues}
          onSubmit={handleSubmit}
          submitting={submitting}
          submitText={isCreate ? "Crear" : "Actualizar"}
        />

        <Button
          variant="secondary"
          className="mt-3"
          onClick={() => navigate(redirectTo)}
        >
          Volver
        </Button>
      </Card.Body>
    </CenteredCard>
  );
}
