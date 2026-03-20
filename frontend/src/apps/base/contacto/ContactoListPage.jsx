
import BaseListPage from "../../../components/listados/BaseListPage";
import ContactoFilter from "./ContactoFilter";

export default function ContactoListPage() {
  return (
    <BaseListPage
      controller="contacto"
      title="Contacto"
      FilterComponent={ContactoFilter}
      columns={[
      { label: "Persona", field: "persona" },
      { label: "Tipo", field: "tipo" }
      ]}
    />
  );
  }
