
import BaseListPage from "../../../components/listados/BaseListPage";
import TipoDocumentoIdentidadFilter from "./TipoDocumentoIdentidadFilter";

export default function TipoDocumentoIdentidadListPage() {
  return (
    <BaseListPage
      controller="tipo-documento-identidad"
      title="TipoDocumentoIdentidad"
      FilterComponent={TipoDocumentoIdentidadFilter}
      columns={[
      { label: "Nombre", field: "nombre" },
      { label: "Descripcion", field: "descripcion" }
      ]}
    />
  );
  }
