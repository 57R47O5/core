
import BaseListPage from "../../../components/listados/BaseListPage";
import { ORCTableColumna } from "../../../components/listados/DataTable";
import VisitaFilter from "./VisitaFilter";

export default function VisitaListPage() {
  return (
    <BaseListPage
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
