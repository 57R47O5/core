import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Container, Row, Col, Card } from "react-bootstrap";
import BaseLayout from "./BaseLayout";

const Home = () => {
  const { user, isAuthenticated } = useContext(AuthContext);

  return (
    <BaseLayout>
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "70vh" }}>
        <Row className="w-100">
          <Col md={{ span: 8, offset: 2 }}>
            <Card className="p-4 text-center shadow-sm">
              <h1 className="mb-3 fw-bold">Bienvenido</h1>

              {isAuthenticated ? (
                <p className="fs-5 text-secondary">
                  ¡Hola, <strong>{user.nombres}</strong>! 👋
                </p>
              ) : (
                <p className="text-muted fs-6 mt-2">
                  Inicia sesión para crear y gestionar tus usuarios.
                </p>
              )}
            </Card>
          </Col>
        </Row>
      </Container>
    </BaseLayout>
  );
};

export default Home;
