
import BaseListPage from "../../../components/listados/BaseListPage";
import DistritoElectoralFilter from "./DistritoElectoralFilter";

export default function DistritoElectoralListPage() {
  return (
    <BaseListPage
      controller="distrito-electoral"
      title="DistritoElectoral"
      FilterComponent={DistritoElectoralFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
