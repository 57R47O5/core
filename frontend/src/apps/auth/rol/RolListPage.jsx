
import BaseListPage from "../../../components/listados/BaseListPage";
import RolFilter from "./RolFilter";

export default function RolListPage() {
  return (
    <BaseListPage
      controller="rol"
      title="Rol"
      FilterComponent={RolFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
