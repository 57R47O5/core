
import BaseListPage from "../../../components/listados/BaseListPage";
import PersonaUserFilter from "./PersonaUserFilter";

export default function PersonaUserListPage() {
  return (
    <BaseListPage
      controller="persona-user"
      title="PersonaUser"
      FilterComponent={PersonaUserFilter}
      columns={[
      { label: "Persona", field: "persona" },
      { label: "User", field: "user" },
      { label: "Principal", field: "principal" }
      ]}
    />
  );
  }
