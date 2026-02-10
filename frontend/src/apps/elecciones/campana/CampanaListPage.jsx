
import BaseListPage from "../../../components/listados/BaseListPage";
import CampanaFilter from "./CampanaFilter";

export default function CampanaListPage() {
  return (
    <BaseListPage
      controller="campana"
      title="Campana"
      FilterComponent={CampanaFilter}
      columns={[
      { label: "Candidato", field: "candidato" },
      { label: "Cargo", field: "cargo" },
      { label: "Distrito", field: "distrito" },
      { label: "Ciclo", field: "ciclo" },
      { label: "Fecha inicio", field: "fecha_inicio" },
      { label: "Fecha fin", field: "fecha_fin" }
      ]}
    />
  );
  }
