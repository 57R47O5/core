
import ABMFilter from "../../../components/filtros/ABMFilter";
import { VotanteFields } from "./VotanteFields";

const VotanteFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Votante"
      fields={VotanteFields}
      controller="votante"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default VotanteFilter;
