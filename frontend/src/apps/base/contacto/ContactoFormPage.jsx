import BaseFormPage from "../../../components/forms/BaseFormPage";
import ContactoForm from "./ContactoForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";


export default function ContactoFormPage() {
  return (
      <ContextGrid
      defaultActive={"base"}
      controller="contacto"
    >
      <ContextTile
          title="Base"
          tileKey="base"
        >
        <BaseFormPage
          FormComponent={ContactoForm}
          titleNew="Nuevo Contacto"
          titleEdit="Editar Contacto"
        />
      </ContextTile>
    </ContextGrid>
  );
}
