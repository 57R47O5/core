
import BaseListPage from "../../../components/listados/BaseListPage";
import DocumentoIdentidadFilter from "./DocumentoIdentidadFilter";

export default function DocumentoIdentidadListPage() {
  return (
    <BaseListPage
      controller="documento-identidad"
      title="DocumentoIdentidad"
      FilterComponent={DocumentoIdentidadFilter}
      columns={[
      { label: "Persona", field: "persona" },
      { label: "Tipo", field: "tipo" },
      { label: "Numero", field: "numero" },
      { label: "Pais emision", field: "pais_emision" },
      { label: "Vigente", field: "vigente" }
      ]}
    />
  );
  }
