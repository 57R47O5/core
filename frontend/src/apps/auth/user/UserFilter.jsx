
import ABMFilter from "../../../components/filtros/ABMFilter";
import { UserFields } from "./UserFields";

const UserFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar User"
      fields={UserFields}
      controller="user"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default UserFilter;
