import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Spinner, Card, Button } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import getAPIBase from "../../api/BaseAPI";

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
  const { id } = useParams();
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
      try {
        const data = await obtener(id);

        // Mezclamos defaults + datos (evita undefineds)
        const populated = {
          ...initialDefaults,
          ...data,
        };

        setInitialValues(populated);
      } catch (error) {
        console.error(error);
        alert("Error cargando instancia");
      }
      setCargando(false);
    };

    if (id) cargarInstancia();
  }, [id]);

  const handleSubmit = async (values) => {
    try {
      setSubmitting(true);

      if (id) {
        await editar(id, values);
        alert("Registro actualizado");
      } else {
        await crear(values);
        alert("Registro creado");
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
        <h3 className="mb-4">{id ? titleEdit : titleNew}</h3>

        <FormComponent
          initialValues={initialValues}
          onSubmit={handleSubmit}
          submitting={submitting}
          submitText={id ? "Actualizar" : "Crear"}
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
