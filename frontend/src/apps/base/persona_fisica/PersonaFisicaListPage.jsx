
import BaseListPage from "../../../components/listados/BaseListPage";
import PersonaFisicaFilter from "./PersonaFisicaFilter";

export default function PersonaFisicaListPage() {
  return (
    <BaseListPage
      controller="persona-fisica"
      title="PersonaFisica"
      FilterComponent={PersonaFisicaFilter}
      columns={[
      { label: "Id", field: "id" },
      { label: "Nombres", field: "nombres" },
      { label: "Apellidos", field: "apellidos" },
      { label: "Fecha nacimiento", field: "fecha_nacimiento" }
      ]}
    />
  );
  }
