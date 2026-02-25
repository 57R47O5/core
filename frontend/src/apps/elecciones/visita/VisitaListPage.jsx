
import BaseListPage from "../../../components/listados/BaseListPage";
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
      { label: "Lugar", field: "lugar" },
      { label: "Fecha", field: "fecha" },
      { label: "Resultado", field: "resultado" },
      { label: "Notas", field: "notas" }
      ]}
    />
  );
  }
