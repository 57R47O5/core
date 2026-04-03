import './../../index.css';
import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import {
  Navbar,
  Nav,
  Container,
  Button,
  Modal,
} from "react-bootstrap";

const NavBar = ({children}) => {
  const navigate = useNavigate();
  const { isAuthenticated, handleLogout } = useContext(AuthContext);
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  const handleLogoutClick = () => setShowLogoutModal(true);
  const handleCloseModal = () => setShowLogoutModal(false);

  const confirmLogout = async () => {
    try {
      await handleLogout();
      navigate("/login");
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
    } finally {
      setShowLogoutModal(false);
    }
  };

  return (
    <>
      <Navbar expand="lg" data-bs-theme="dark" className="mb-4" style={{backgroundColor: "var(--allports-900)"}}>
        <Container>
          <Navbar.Brand as={Link} to="/" className="mx-auto">
            Agora
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="main-navbar" />
          <Navbar.Collapse id="main-navbar">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">Inicio</Nav.Link>

              {!isAuthenticated && (
                <>                  
                  <Nav.Link as={Link} to="/login">Iniciar Sesión</Nav.Link>
                </>
              )}
              
            </Nav>

            {/* Botón de logout */}
            {isAuthenticated && (
              <Button variant="outline-light" onClick={handleLogoutClick}>
                Cerrar Sesión
              </Button>
            )}
          </Navbar.Collapse>
        </Container>
        <main>
          {children}
        </main>
      </Navbar>

      {/* Modal de confirmación */}
      <Modal show={showLogoutModal} onHide={handleCloseModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirmar Cierre de Sesión</Modal.Title>
        </Modal.Header>
        <Modal.Body>¿Estás seguro de que deseas cerrar sesión?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cancelar
          </Button>
          <Button variant="danger" onClick={confirmLogout}>
            Cerrar Sesión
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default NavBar;
