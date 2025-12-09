import { useState } from "react";
import { Card, Table, Row, Col, Button, Form as RBForm } from "react-bootstrap";
import { Formik, Form } from "formik";
import DatePickerFormik from "../forms/DatePickerFomik";
import SelectFormik from "../forms/SelectFormik";
import { diarios } from "./TurnoAPI"

export default function TurnosDiariosPage() {
  const [turnos, setTurnos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const cargarTurnos = async (fecha, odontologo) => {
    if (!fecha) return;

    setLoading(true);
    setError("");

    try {
      const data = await diarios(fecha, odontologo);
      setTurnos(data);
    } catch (err) {
      setError("Error al cargar los turnos");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <Card className="p-4 mt-4">
      <h3 className="mb-4 text-center">Turnos del día</h3>

      <Formik
        initialValues={{
          fecha: "",
          odontologo: "",
        }}
        onSubmit={(values) => {
          cargarTurnos(values.fecha, values.odontologo);
        }}
      >
        {({ values }) => (
          <Form>
            <Row className="mb-3">
              <Col md={4}>
                <RBForm.Label>Fecha</RBForm.Label>
                <DatePickerFormik name="fecha" />
              </Col>

              <Col md={5}>
                <RBForm.Label>Odontólogo (opcional)</RBForm.Label>
                <SelectFormik
                  name="odontologo"
                  endpoint="usuarios/medicos"
                  placeholder="Seleccione un odontólogo"
                />
              </Col>

              <Col md={3} className="d-flex align-items-end">
                <Button
                  type="submit"
                  variant="primary"
                  className="w-100"
                  disabled={loading}
                >
                  {loading ? "Buscando..." : "Buscar"}
                </Button>
              </Col>
            </Row>
          </Form>
        )}
      </Formik>

      <hr />

      {error && <p className="text-danger text-center">{error}</p>}

      {/* Tabla de turnos */}
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Hora</th>
            <th>Paciente</th>
            <th>Odontólogo</th>
          </tr>
        </thead>
        <tbody>
          {turnos.length === 0 ? (
            <tr>
              <td colSpan="5" className="text-center">
                {loading ? "Cargando..." : "No hay turnos para esta fecha"}
              </td>
            </tr>
          ) : (
            turnos.map((t) => (
              <tr key={t.id}>
                <td>{t.hora_inicio}</td>
                <td>{t.paciente}</td>
                <td>{t.odontologo}</td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </Card>
  );
}
