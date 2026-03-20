
import BaseListPage from "../../../components/listados/BaseListPage";
import TipoContactoFilter from "./TipoContactoFilter";

export default function TipoContactoListPage() {
  return (
    <BaseListPage
      controller="tipo-contacto"
      title="TipoContacto"
      FilterComponent={TipoContactoFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
