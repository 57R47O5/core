
import BaseListPage from "../../../components/listados/BaseListPage";
import { ORCTableColumna } from "../../../components/listados/DataTable";
import UserFilter from "./UserFilter";

export default function UserListPage() {
  return (
    <BaseListPage
      controller="user"
      title="Usuarios"
      FilterComponent={UserFilter}
      columns={[
      { label: "Id", field: "id" },
      { label: "Username", field: "username" },
      { label: "Activo", field: "is_active", tipo:ORCTableColumna.BOOLEANO },
      { label: "Fecha Creacion", field: "created_at", tipo: ORCTableColumna.FECHA }
      ]}
    />
  );
  }
