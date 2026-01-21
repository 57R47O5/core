
import BaseListPage from "../../components/listados/BaseListPage";
import MonedaFilter from "./MonedaFilter";

export default function MonedaListPage() {
  return (
    <BaseListPage
      controller="moneda"
      title="Moneda"
      FilterComponent={MonedaFilter}
      columns={[
      { label: "Id", field: "id" },
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" },
      { label: "Simbolo", field: "simbolo" }
      ]}
    />
  );
  }
