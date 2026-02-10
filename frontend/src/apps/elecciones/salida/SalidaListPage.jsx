
import BaseListPage from "../../../components/listados/BaseListPage";
import SalidaFilter from "./SalidaFilter";

export default function SalidaListPage() {
  return (
    <BaseListPage
      controller="salida"
      title="Salida"
      FilterComponent={SalidaFilter}
      columns={[
      { label: "Campana", field: "campana" },
      { label: "Colaborador", field: "colaborador" },
      { label: "Fecha", field: "fecha" },
      { label: "Estado", field: "estado" }
      ]}
    />
  );
  }
