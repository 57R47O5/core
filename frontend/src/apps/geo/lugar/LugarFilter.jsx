
import ABMFilter from "../../../components/filtros/ABMFilter";
import { LugarFields } from "./LugarFields";

const LugarFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Lugar"
      fields={LugarFields}
      controller="lugar"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default LugarFilter;
