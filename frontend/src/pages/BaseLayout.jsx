import { useState } from "react";
import { Container } from "react-bootstrap";

function BaseLayout({ children }) {
  const [tema, setTema] = useState("light");

  const cambiarTema = () => {
    setTema((t) => (t === "light" ? "dark" : "light"));
  };

  return (
    <div data-bs-theme={tema}>
      <Container fluid className="py-3">
        <button className="btn btn-secondary mb-3" onClick={cambiarTema}>
          Cambiar a {tema === "light" ? "Dark" : "Light"}
        </button>

        {children}
      </Container>
    </div>
  );
}

export default BaseLayout;
