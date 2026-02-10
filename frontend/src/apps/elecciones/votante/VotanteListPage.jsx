
import BaseListPage from "../../../components/listados/BaseListPage";
import VotanteFilter from "./VotanteFilter";

export default function VotanteListPage() {
  return (
    <BaseListPage
      controller="votante"
      title="Votante"
      FilterComponent={VotanteFilter}
      columns={[
      { label: "Persona", field: "persona" },
      { label: "Distrito", field: "distrito" },
      { label: "Seccional", field: "seccional" }
      ]}
    />
  );
  }
