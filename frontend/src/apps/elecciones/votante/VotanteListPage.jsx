
import BaseListPage from "../../../components/listados/BaseListPage";
import VotanteFilter from "./VotanteFilter";

export default function VotanteListPage() {
  return (
    <BaseListPage
      controller="votante"
      title="Votante"
      FilterComponent={VotanteFilter}
      columns={[
      { label: "Nombres", field: "nombres" },
      { label: "Apellidos", field: "apellidos" },
      { label: "Distrito", field: "distrito" }
      ]}
    />
  );
  }
