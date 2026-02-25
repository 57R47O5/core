
import BaseListPage from "../../../components/listados/BaseListPage";
import CicloElectoralFilter from "./CicloElectoralFilter";

export default function CicloElectoralListPage() {
  return (
    <BaseListPage
      controller="ciclo-electoral"
      title="CicloElectoral"
      FilterComponent={CicloElectoralFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
