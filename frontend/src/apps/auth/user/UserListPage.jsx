
import BaseListPage from "../../../components/listados/BaseListPage";
import UserFilter from "./UserFilter";

export default function UserListPage() {
  return (
    <BaseListPage
      controller="user"
      title="Persona Fisica"
      FilterComponent={UserFilter}
      columns={[
      { label: "Id", field: "id" },
      { label: "Username", field: "username" },
      { label: "Activo", field: "activo" },
      { label: "Fecha Creacion", field: "created_at" }
      ]}
    />
  );
  }
