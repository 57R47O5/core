
import ABMFilter from "../../../components/filtros/ABMFilter";
import { SeccionalFields } from "./SeccionalFields";

const SeccionalFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Seccional"
      fields={SeccionalFields}
      controller="seccional"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default SeccionalFilter;
