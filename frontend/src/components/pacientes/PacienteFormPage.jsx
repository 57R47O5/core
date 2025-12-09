import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Spinner, Card, Button } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import PacienteAPI from "./PacienteAPI";
import PacienteForm from "./PacienteForm";

const PacienteFormPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [initialValues, setInitialValues] = useState({
    nombre: "",
    apellido: "",
    dni: "",
    telefono: "",
    email: "",
    notas: "",
  });

  const [cargando, setCargando] = useState(!!id);
  const [submitting, setSubmitting] = useState(false);

  // Cargar paciente en modo edición
  useEffect(() => {
    const cargarPaciente = async () => {
      try {
        const data = await PacienteAPI.obtener(id);
        setInitialValues({
          nombre: data.nombre || "",
          apellido: data.apellido || "",
          dni: data.dni || "",
          telefono: data.telefono || "",
          email: data.email || "",
          notas: data.notas || "",
        });
      } catch (error) {
        console.error(error);
        alert("Error cargando paciente");
      }
      setCargando(false);
    };

    if (id) cargarPaciente();
  }, [id]);

  const handleSubmit = async (values) => {
    try {
      setSubmitting(true);

      if (id) {
        await PacienteAPI.editar(id, values);
        alert("Paciente actualizado");
      } else {
        await PacienteAPI.crear(values);
        alert("Paciente creado");
      }
      navigate("/pacientes");
    } catch (error) {
      console.error(error);
      alert("Error al guardar el paciente");
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
    <CenteredCard >
      <Card.Body>
        <h3 className="mb-4">{id ? "Editar Paciente" : "Nuevo Paciente"}</h3>

        <PacienteForm
          initialValues={initialValues}
          onSubmit={handleSubmit}
          submitting={submitting}
          submitText={id ? "Actualizar" : "Crear"}
        />

        <Button
          variant="secondary"
          className="mt-3"
          onClick={() => navigate("/pacientes")}
        >
          Volver
        </Button>
      </Card.Body>
    </CenteredCard>
  );
};

export default PacienteFormPage;
