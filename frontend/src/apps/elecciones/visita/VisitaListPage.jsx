
import MapListPage from "../../../components/listados/MapListPage";
import { ORCTableColumna } from "../../../components/listados/DataTable";
import VisitaFilter from "./VisitaFilter";

export default function VisitaListPage() {
  return (
    <MapListPage
      controller="visita"
      title="Visita"
      FilterComponent={VisitaFilter}
       colorScale={{
        field: "resultado_id",
        domain: [1, 4],
        colors: [
          "var(--map-red)",
          "var(--map-yellow)",
          "var(--map-green)"
        ]
      }}
    />
  );
  }
