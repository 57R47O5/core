
import ABMFilter from "../../../components/filtros/ABMFilter";
import { PersonaFisicaFields } from "./PersonaFisicaFields";

const PersonaFisicaFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar PersonaFisica"
      fields={PersonaFisicaFields}
      controller="persona-fisica"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default PersonaFisicaFilter;
