
import ABMFilter from "../../../components/filtros/ABMFilter";
import { ContactoFields } from "./ContactoFields";

const ContactoFilter = ({ onSearch, loading }) => {
  
  return (
    <ABMFilter
      title="Filtrar Contacto"
      fields={ContactoFields}
      controller="contacto"
      onSearch={onSearch}
      loading={loading}
    />
  );
};

export default ContactoFilter;
