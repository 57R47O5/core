
import BaseListPage from "../../../components/listados/BaseListPage";
import SeccionalFilter from "./SeccionalFilter";

export default function SeccionalListPage() {
  return (
    <BaseListPage
      controller="seccional"
      title="Seccional"
      FilterComponent={SeccionalFilter}
      columns={[
      { label: "Zona", field: "zona" },
      { label: "Campana", field: "campana" }
      ]}
    />
  );
  }
