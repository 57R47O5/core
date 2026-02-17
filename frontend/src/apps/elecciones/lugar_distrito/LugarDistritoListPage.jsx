
import BaseListPage from "../../../components/listados/BaseListPage";
import LugarDistritoFilter from "./LugarDistritoFilter";

export default function LugarDistritoListPage() {
  return (
    <BaseListPage
      controller="lugar-distrito"
      title="LugarDistrito"
      FilterComponent={LugarDistritoFilter}
      columns={[
      { label: "Distrito", field: "distrito" },
      { label: "Lugar", field: "lugar" }
      ]}
    />
  );
  }
