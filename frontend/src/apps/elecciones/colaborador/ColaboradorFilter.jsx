
import ABMFilter from "../../../components/filtros/ABMFilter";
import { ColaboradorFields } from "./ColaboradorFields";

const ColaboradorFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Colaborador"
      fields={ColaboradorFields}
      controller="colaborador"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default ColaboradorFilter;
