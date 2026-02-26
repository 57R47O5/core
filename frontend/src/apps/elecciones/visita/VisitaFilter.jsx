
import ABMFilter from "../../../components/filtros/ABMFilter";
import { VisitaFields } from "./VisitaFields";

const VisitaFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Visita"
      fields={VisitaFields}
      controller="visita"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default VisitaFilter;
