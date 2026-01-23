import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import {
  Navbar,
  Nav,
  Container,
  Button,
  Modal,
  NavDropdown,
} from "react-bootstrap";

const NavBar = ({children}) => {
  const navigate = useNavigate();
  const { isAuthenticated, handleLogout, user } = useContext(AuthContext);
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
      <Navbar expand="lg" bg="primary" data-bs-theme="dark" className="mb-4">
        <Container>
          <Navbar.Brand as={Link} to="/">
            NombreProyecto
          </Navbar.Brand>

          <Navbar.Toggle aria-controls="main-navbar" />
          <Navbar.Collapse id="main-navbar">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">Inicio</Nav.Link>

              {!isAuthenticated && (
                <>
                  <Nav.Link as={Link} to="/register">Registro</Nav.Link>
                  <Nav.Link as={Link} to="/login">Iniciar Sesión</Nav.Link>
                </>
              )}

              {/* {isAuthenticated && (
                <>
                  <Nav.Link as={Link} to="/usuarios">Usuarios</Nav.Link>

                  

                  <NavDropdown title="Mi Cuenta" id="user-dropdown">
                    <NavDropdown.Item as={Link} to={`/usuarios/${user.id}`}>
                      Perfil
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item onClick={handleLogoutClick}>
                      Cerrar Sesión
                    </NavDropdown.Item>
                  </NavDropdown>
                </>
              )} */}
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
