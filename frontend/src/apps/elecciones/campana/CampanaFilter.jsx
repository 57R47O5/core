
import ABMFilter from "../../../components/filtros/ABMFilter";
import { CampanaFields } from "./CampanaFields";

const CampanaFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Campaña"
      fields={CampanaFields}
      controller="campana"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default CampanaFilter;
