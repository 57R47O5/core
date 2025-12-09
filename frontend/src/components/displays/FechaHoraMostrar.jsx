import { Badge } from "react-bootstrap";

export default function FechaHoraMostrar({
  value,
  mode = "datetime", // "date", "time", "datetime"
  variant = "badge",  // "badge" | "text"
  className = "",
}) {
  if (!value) return <span>—</span>;

  const fecha = new Date(value);

  const formatDate = (d) =>
    d.toLocaleDateString("es-AR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });

  const formatTime = (d) =>
    d.toLocaleTimeString("es-AR", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });

  let output = "";
  if (mode === "date") output = formatDate(fecha);
  else if (mode === "time") output = formatTime(fecha);
  else output = `${formatDate(fecha)} ${formatTime(fecha)}`;

  // --- Nueva variante para links o botones ---
  if (variant === "text") {
    return <span className={className}>{output}</span>;
  }

  // Variante anterior (badge)
  return (
    <Badge bg="light" text="dark" className={className}>
      {output}
    </Badge>
  );
}
