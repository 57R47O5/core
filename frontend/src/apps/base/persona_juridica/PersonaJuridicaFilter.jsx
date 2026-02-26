
import ABMFilter from "../../../components/filtros/ABMFilter";
import { PersonaJuridicaFields } from "./PersonaJuridicaFields";

const PersonaJuridicaFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar PersonaJuridica"
      fields={PersonaJuridicaFields}
      controller="persona-juridica"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default PersonaJuridicaFilter;
