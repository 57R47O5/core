import BaseListPage from "../../components/listados/BaseListPage";
import PacientesFilter from "./PacientesFilter";

export default function PacientesListPage() {
  return (
    <BaseListPage
      controller="paciente"
      title="Pacientes"
      FilterComponent={PacientesFilter}
      columns={[
        { label: "Nombre", field: "nombre" },
        { label: "Apellido", field: "apellido" },
        { label: "DNI", field: "dni" },
        { label: "Teléfono", field: "telefono" },
        { label: "Email", field: "email" },
      ]}
    />
  );
}
