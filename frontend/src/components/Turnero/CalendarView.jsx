import React from "react";
import { useNavigate } from "react-router-dom";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

const CalendarView = ({ turnos, tipo, fecha }) => {

  const navigate = useNavigate();

  const view = {
    diario: "timeGridDay",
    semanal: "timeGridWeek",
    mensual: "dayGridMonth"
  }[tipo];

  const eventos = turnos.map(t => ({
    title: `${t.paciente} - ${t.odontologo}`,
    start: `${t.fecha_inicio}`,
    end: `${t.fecha_fin}`,
    extendedProps: { ...t }
  }));

  return (
    <FullCalendar
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView={view}
      initialDate={fecha}
      events={eventos}
      height="80vh"
      locale="es"
      headerToolbar={{
        left: "",
        center: "title",
        right: ""
      }}

      eventClick={(info) => {
        const turnoId = info.event._def.extendedProps.id;
        navigate(`/turnos/${turnoId}`);
      }}
    />
  );
};

export default CalendarView;
