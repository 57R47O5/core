import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button
} from "react-bootstrap";

const LoginPage = () => {
  const navigate = useNavigate();
  const { handleLogin } = useContext(AuthContext);
  const [form, setForm] = useState({ identifier: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await handleLogin(form);
    navigate("/");
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "80vh" }}>
      <Row className="w-100" style={{ maxWidth: "420px" }}>
        <Col>
          <Card className="p-4 shadow-sm">
            <h2 className="text-center mb-4">Iniciar sesión</h2>

            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="identifier">
                <Form.Label>Usuario</Form.Label>
                <Form.Control
                  type="text"
                  name="identifier"
                  value={form.identifier}
                  onChange={handleChange}
                  placeholder="Ingrese su usuario"
                />
              </Form.Group>

              <Form.Group className="mb-4" controlId="password">
                <Form.Label>Contraseña</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Ingrese su contraseña"
                />
              </Form.Group>

              <Button type="submit" variant="primary" className="w-100">
                Ingresar
              </Button>
            </Form>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;
