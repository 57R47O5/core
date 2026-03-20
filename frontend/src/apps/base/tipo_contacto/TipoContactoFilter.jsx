
import ABMFilter from "../../../components/filtros/ABMFilter";
import { TipoContactoFields } from "./TipoContactoFields";

const TipoContactoFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar TipoContacto"
      fields={TipoContactoFields}
      controller="tipo-contacto"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default TipoContactoFilter;
