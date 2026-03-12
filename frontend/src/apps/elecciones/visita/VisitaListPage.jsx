
import MapListPage from "../../../components/listados/MapListPage";
import { ORCTableColumna } from "../../../components/listados/DataTable";
import VisitaFilter from "./VisitaFilter";

export default function VisitaListPage() {
  return (
    <MapListPage
      controller="visita"
      title="Visita"
      FilterComponent={VisitaFilter}
      columns={[
      { label: "Salida", field: "salida" },
      { label: "Votante", field: "votante" },
      { label: "Fecha", field: "fecha", tipo:ORCTableColumna.FECHA_HORA },
      { label: "Resultado", field: "resultado" },
      ]}
    />
  );
  }
