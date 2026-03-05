
import ABMFilter from "../../../components/filtros/ABMFilter";
import { PermisoFields } from "./PermisoFields";

const PermisoFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Permiso"
      fields={PermisoFields}
      controller="permiso"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default PermisoFilter;
