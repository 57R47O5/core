
import ABMFilter from "../../../components/filtros/ABMFilter";
import { RolFields } from "./RolFields";

const RolFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Rol"
      fields={RolFields}
      controller="rol"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default RolFilter;
