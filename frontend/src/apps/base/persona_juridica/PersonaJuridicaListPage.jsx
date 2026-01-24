
import BaseListPage from "../../../components/listados/BaseListPage";
import PersonaJuridicaFilter from "./PersonaJuridicaFilter";

export default function PersonaJuridicaListPage() {
  return (
    <BaseListPage
      controller="persona-juridica"
      title="PersonaJuridica"
      FilterComponent={PersonaJuridicaFilter}
      columns={[
      { label: "Persona", field: "persona" },
      { label: "Razon social", field: "razon_social" },
      { label: "Nombre fantasia", field: "nombre_fantasia" }
      ]}
    />
  );
  }
