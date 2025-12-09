import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { obtenerUsuarios } from "../../api/UsuariosAPI";
import BaseLayout from "../BaseLayout";
import {
  Container,
  Row,
  Col,
  Button,
  Table,
  Card,
  Spinner
} from "react-bootstrap";

export default function UsuarioList() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cargarUsuarios = async () => {
      try {
        const data = await obtenerUsuarios();
        setUsuarios(data);
      } catch (error) {
        console.error("Error al cargar usuarios:", error);
      } finally {
        setLoading(false);
      }
    };

    cargarUsuarios();
  }, []);

  return (
    <BaseLayout>
      <Container>
        <Row className="mb-4">
          <Col>
            <h1 className="mb-3">Usuarios</h1>
          </Col>
          <Col className="text-end">
            <Button as={Link} to="/usuarios/nuevo" variant="primary">
              Crear nuevo
            </Button>
          </Col>
        </Row>

        <Card>
          <Card.Body>
            {loading ? (
              <div className="text-center py-5">
                <Spinner animation="border" role="status" />
              </div>
            ) : usuarios.length > 0 ? (
              <Table striped bordered hover responsive>
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Rol</th>
                    <th>Activo</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {usuarios.map((u) => (
                    <tr key={u.id}>
                      <td>{u.username}</td>
                      <td>{u.email}</td>
                      <td>{u.rol}</td>
                      <td>{u.activo ? "Sí" : "No"}</td>
                      <td>
                        <Button
                          as={Link}
                          to={`/usuarios/${u.id}`}
                          variant="outline-primary"
                          size="sm"
                        >
                          Editar
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            ) : (
              <p className="text-muted text-center mb-0">
                No hay usuarios cargados.
              </p>
            )}
          </Card.Body>
        </Card>
      </Container>
    </BaseLayout>
  );
}
