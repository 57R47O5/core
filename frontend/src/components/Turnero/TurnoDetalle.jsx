import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button, Spinner, Card, Alert, Row, Col, Modal } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import { Formik, Form, Field } from "formik";
import FechaHoraMostrar from "../displays/FechaHoraMostrar";
import * as Yup from "yup";

import {
  obtener,
  editar,
  eliminar
} from "./TurnoAPI.jsx"; 

// =========================
//   VALIDACIÓN FORM
// =========================
const TurnoSchema = Yup.object().shape({
  fecha: Yup.string().required("La fecha es obligatoria"),
  hora_inicio: Yup.string().required("La hora de inicio es obligatoria"),
  hora_fin: Yup.string().nullable(),
  estado: Yup.string().required("El estado es obligatorio"),
  notas: Yup.string(),
});

export default function TurnoDetalle() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [turno, setTurno] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");
  const [showDelete, setShowDelete] = useState(false);

  // =========================
  //   Cargar datos
  // =========================
  useEffect(() => {
    const fetchTurno = async () => {
      try {
        const resp = await obtener(id);
        setTurno(resp);
      } catch (err) {
        setError("No se pudo cargar el turno.");
      } finally {
        setLoading(false);
      }
    };

    fetchTurno();
  }, [id]);

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  if (!turno) {
    return <Alert variant="danger">Turno no encontrado</Alert>;
  }

  return (
    <CenteredCard className="mt-4 shadow-sm">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <h4 className="m-0">Detalle del Turno</h4>

        {!editing && (
          <div>
            <Button variant="primary" onClick={() => setEditing(true)}>
              Editar
            </Button>{" "}
            <Button variant="danger" onClick={() => setShowDelete(true)}>
              Eliminar
            </Button>
          </div>
        )}
      </Card.Header>

      <Card.Body>
        {error && <Alert variant="danger">{error}</Alert>}

        {!editing ? (
          // ========================
          //   MODO VISUALIZACIÓN
          // ========================
          <div>
            <Row>
              <Col md={6}>
                <p>
                  <strong>Paciente:</strong>{" "}
                  <span
                    className="text-primary fw-semibold link"
                    style={{ cursor: "pointer" }}
                    onClick={() => navigate(`/pacientes/${turno.paciente.id}`)}
                  >
                    {turno.paciente.nombre} {turno.paciente.apellido}
                  </span>
                </p>
                 <p>
                    <strong>Odontólogo:</strong>{" "}
                    <span
                      className="text-primary fw-semibold link"
                      style={{ cursor: "pointer" }}
                      onClick={() => navigate(`/usuarios/${turno.odontologo.id}`)}
                    >
                      {turno.odontologo.nombres} {turno.odontologo.apellidos}
                    </span>
                  </p>
                <p><strong>Estado:</strong> {turno.estado}</p>
              </Col>

              <Col md={6}>
                <p>
                  <strong>Fecha Inicio:</strong>{" "}
                  <Button
                    variant="link"
                    className="p-0 fw-semibold d-inline-flex align-items-center"
                    onClick={() =>
                      navigate(`/turnos?tipo=diario&fecha=${turno.fecha_inicio}`)
                    }
                  >
                    <FechaHoraMostrar
                      value={turno.fecha_inicio}
                      mode="date"
                      variant="light"
                      className="me-1"
                    />
                    <i className="bi bi-calendar-day"></i>
                  </Button>
                </p>

                <p>
                  <strong>Fecha Fin:</strong>{" "}
                  {turno.fecha_fin ? (
                    <FechaHoraMostrar
                      value={turno.fecha_fin}
                      mode="date"
                      variant="light"
                    />
                  ) : (
                    "—"
                  )}
                </p>

              </Col>
            </Row>

            <p><strong>Notas:</strong></p>
            <div className="p-2 bg-light rounded">{turno.notas || "Sin notas"}</div>
          </div>
        ) : (
          // ========================
          //     MODO EDICIÓN
          // ========================
          <Formik
            initialValues={turno}
            validationSchema={TurnoSchema}
            onSubmit={async (values, { setSubmitting }) => {
              try {
                await editar(turno.id, values);
                setTurno(values);
                setEditing(false);
              } catch (err) {
                setError("Error al guardar los cambios.");
              } finally {
                setSubmitting(false);
              }
            }}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form>
                <Row className="mb-3">
                  <Col md={6}>
                    <label>Fecha Inicio</label>
                    <Field name="fecha_inicio" type="date" className="form-control" />
                    {touched.fecha_inicio && errors.fecha_inicio && (
                      <div className="text-danger">{errors.fecha}</div>
                    )}
                  </Col>


                  <Col md={3}>
                    <label>Fecha Fin</label>
                    <Field name="fecha_fin" type="time" className="form-control" />
                  </Col>
                </Row>

                <Row className="mb-3">
                  <Col md={6}>
                    <label>Estado</label>
                    <Field as="select" name="estado" className="form-control">
                      <option value="pendiente">Pendiente</option>
                      <option value="confirmado">Confirmado</option>
                      <option value="cancelado">Cancelado</option>
                    </Field>
                  </Col>
                </Row>

                <div className="mb-3">
                  <label>Notas</label>
                  <Field as="textarea" name="notas" className="form-control" rows={4} />
                </div>

                <div className="d-flex justify-content-end">
                  <Button
                    variant="secondary"
                    className="me-2"
                    onClick={() => setEditing(false)}
                  >
                    Cancelar
                  </Button>

                  <Button type="submit" variant="success" disabled={isSubmitting}>
                    {isSubmitting ? "Guardando..." : "Guardar cambios"}
                  </Button>
                </div>
              </Form>
            )}
          </Formik>
        )}
      </Card.Body>

      {/* ============================
          MODAL ELIMINAR TURNO
      ============================ */}
      <Modal show={showDelete} onHide={() => setShowDelete(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Eliminar Turno</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          ¿Estás seguro de que deseas eliminar este turno? Esta acción no se puede deshacer.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDelete(false)}>
            Cancelar
          </Button>
          <Button
            variant="danger"
            onClick={async () => {
              try {
                await eliminar(turno.id);
                navigate("/turnos");
              } catch (err) {
                setError("Error al eliminar el turno.");
              }
            }}
          >
            Eliminar
          </Button>
        </Modal.Footer>
      </Modal>
    </CenteredCard>
  );
}
