
import BaseListPage from "../../../components/listados/BaseListPage";
import PermisoFilter from "./PermisoFilter";

export default function PermisoListPage() {
  return (
    <BaseListPage
      controller="permiso"
      title="Permiso"
      FilterComponent={PermisoFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
