
import BaseListPage from "../../components/listados/BaseListPage";
import UserRolFilter from "./UserRolFilter";

export default function UserRolListPage() {
  return (
    <BaseListPage
      controller="user-rol"
      title="UserRol"
      FilterComponent={UserRolFilter}
      columns={[
      { label: "User", field: "user" },
      { label: "Rol", field: "rol" }
      ]}
    />
  );
  }
