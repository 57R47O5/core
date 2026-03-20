import BaseFormPage from "../../../components/forms/BaseFormPage";
import TipoContactoForm from "./TipoContactoForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";


export default function TipoContactoFormPage() {
  return (
      <ContextGrid
      defaultActive={"base"}
      controller="tipo-contacto"
    >
      <ContextTile
          title="Base"
          tileKey="base"
        >
        <BaseFormPage
          FormComponent={TipoContactoForm}
          titleNew="Nuevo TipoContacto"
          titleEdit="Editar TipoContacto"
        />
      </ContextTile>
    </ContextGrid>
  );
}
