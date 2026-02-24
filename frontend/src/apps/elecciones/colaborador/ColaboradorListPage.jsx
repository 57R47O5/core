
import BaseListPage from "../../../components/listados/BaseListPage";
import ColaboradorFilter from "./ColaboradorFilter";

export default function ColaboradorListPage() {
  return (
    <BaseListPage
      controller="colaborador"
      title="Colaborador"
      FilterComponent={ColaboradorFilter}
      columns={[
      { label: "Nombres", field: "nombres" },
      { label: "Apellidos", field: "apellidos" }
      ]}
    />
  );
  }
