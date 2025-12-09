import React, { useEffect, useState } from "react";
import { Container, Spinner, Button, Offcanvas } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import Filters from "./Filters";
import CalendarView from "./CalendarView";
import { getTurnos } from "./TurnoAPI";
import { BsFunnel } from "react-icons/bs";

const TurneroPage = () => {
  const [filtros, setFiltros] = useState({
    tipo: "diario",
    fecha_inicio: new Date().toISOString().slice(0, 10),
    odontologo: "",
    paciente: "",
  });

  const [turnos, setTurnos] = useState([]);
  const [loading, setLoading] = useState(false);

  // Estado para el sidebar Offcanvas
  const [showFilters, setShowFilters] = useState(false);

  const handleShow = () => setShowFilters(true);
  const handleClose = () => setShowFilters(false);

  const cargarTurnos = async () => {
    setLoading(true);
    const data = await getTurnos(filtros);
    setTurnos(data);
    setLoading(false);
  };

  useEffect(() => {
    cargarTurnos();
  }, [filtros]);

  return (
    <div>

      {/* --- BOTÓN PARA ABRIR FILTROS (FIJO A LA IZQUIERDA) --- */}
      <Button
        variant="primary"
        onClick={handleShow}
        className="filters-toggle-btn shadow-sm"
      >
        <BsFunnel size={20} className="me-2" />
        Filtros
      </Button>

      {/* --- SIDEBAR OFFCANVAS --- */}
      <Offcanvas
        show={showFilters}
        onHide={handleClose}
        placement="start"
        backdrop={false}
        scroll
      >
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Filtros</Offcanvas.Title>
        </Offcanvas.Header>

        <Offcanvas.Body>
          <Filters filtros={filtros} setFiltros={setFiltros} />
        </Offcanvas.Body>
      </Offcanvas>

      {/* --- CONTENIDO PRINCIPAL --- */}
      <Container className="mt-4">
        <CenteredCard className="p-3">
          {loading ? (
            <div className="text-center py-5">
              <Spinner animation="border" />
            </div>
          ) : (
            <CalendarView
              turnos={turnos}
              tipo={filtros.tipo}
              fecha={filtros.fecha}
            />
          )}
        </CenteredCard>
      </Container>
    </div>
  );
};

export default TurneroPage;
