import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Table, Button, Card, Form as RBForm, Spinner } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";

import PacienteAPI from "./PacienteAPI";


// Validación del form de filtros
const FiltroSchema = Yup.object().shape({
  nombre: Yup.string().nullable(),
  apellido: Yup.string().nullable(),
  dni: Yup.string().nullable(),
  fecha_desde: Yup.date().nullable(),
  fecha_hasta: Yup.date().nullable(),
});

const PacientesListPage = () => {
  const navigate = useNavigate();

  const [pacientes, setPacientes] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchPacientes = async (values = {}) => {
    setLoading(true);
    try {
      const data = await PacienteAPI.buscar(values);
      setPacientes(data);
    } catch (error) {
      console.error("Error al obtener pacientes:", error);
      alert("Hubo un error al cargar los pacientes");
    }
    setLoading(false);
  };

  // Cargar pacientes al entrar
  useEffect(() => {
    fetchPacientes();
  }, []);

  return (
    <div className="container">
      <h2 className="mb-4">Pacientes</h2>

      {/* -------------------- FORM DE FILTROS -------------------- */}

      <CenteredCard >
        <Card.Body>
          <h5 className="mb-3">Filtrar pacientes</h5>

          <Formik
            initialValues={{
              nombre: "",
              apellido: "",
              dni: "",
              fecha_desde: "",
              fecha_hasta: "",
            }}
            validationSchema={FiltroSchema}
            onSubmit={(values) => fetchPacientes(values)}
          >
            {({ errors, touched }) => (
              <Form>
                <div className="row">

                  <div className="col-md-3 mb-3">
                    <RBForm.Label>Nombre</RBForm.Label>
                    <Field
                      name="nombre"
                      className="form-control"
                    />
                  </div>

                  <div className="col-md-3 mb-3">
                    <RBForm.Label>Apellido</RBForm.Label>
                    <Field
                      name="apellido"
                      className="form-control"
                    />
                  </div>

                  <div className="col-md-2 mb-3">
                    <RBForm.Label>DNI</RBForm.Label>
                    <Field name="dni" className="form-control" />
                  </div>

                  <div className="col-md-2 mb-3">
                    <RBForm.Label>Desde</RBForm.Label>
                    <Field name="fecha_desde" type="date" className="form-control" />
                  </div>

                  <div className="col-md-2 mb-3">
                    <RBForm.Label>Hasta</RBForm.Label>
                    <Field name="fecha_hasta" type="date" className="form-control" />
                  </div>
                </div>

                <div className="text-end">
                  <Button type="submit" variant="primary">
                    Buscar
                  </Button>
                </div>
              </Form>
            )}
          </Formik>
        </Card.Body>
      </CenteredCard>

      {/* -------------------- TABLA DE PACIENTES -------------------- */}

      <CenteredCard>
        <Card.Body>
          <h5 className="mb-3">Resultados</h5>

          {loading ? (
            <div className="text-center my-4">
              <Spinner animation="border" />
            </div>
          ) : (
            <Table striped bordered hover>
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Apellido</th>
                  <th>DNI</th>
                  <th>Teléfono</th>
                  <th>Email</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {pacientes.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center">
                      No se encontraron pacientes
                    </td>
                  </tr>
                ) : (
                  pacientes.map((p) => (
                    <tr key={p.id}>
                      <td>{p.nombre}</td>
                      <td>{p.apellido}</td>
                      <td>{p.dni || "-"}</td>
                      <td>{p.telefono || "-"}</td>
                      <td>{p.email || "-"}</td>
                      <td>
                        <Button
                          size="sm"
                          onClick={() => navigate(`/pacientes/${p.id}`)}
                        >
                          Editar
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </CenteredCard>
    </div>
  );
};

export default PacientesListPage;
