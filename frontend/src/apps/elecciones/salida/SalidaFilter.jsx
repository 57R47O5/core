
import ABMFilter from "../../../components/filtros/ABMFilter";
import { SalidaFields } from "./SalidaFields";

const SalidaFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Salida"
      fields={SalidaFields}
      controller="salida"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default SalidaFilter;
