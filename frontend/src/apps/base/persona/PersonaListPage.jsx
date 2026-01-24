
import BaseListPage from "../../../components/listados/BaseListPage";
import PersonaFilter from "./PersonaFilter";

export default function PersonaListPage() {
  return (
    <BaseListPage
      controller="persona"
      title="Persona"
      FilterComponent={PersonaFilter}
      columns={[

      ]}
    />
  );
  }
