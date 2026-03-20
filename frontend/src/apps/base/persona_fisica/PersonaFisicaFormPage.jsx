import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";
import { useRouteMode } from "../../../hooks/useRouteMode";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { DocumentosPersona } from "../documento_identidad/DocumentoIdentidadForm";

export default function PersonaFisicaFormPage() {
  const { isEdit } = useRouteMode();

  return (
    <ContextGrid
      defaultActive={"datos-personales"}
      controller={"persona-fisica"}
    > 
      <ContextTile
        title="Datos Personales"
        tileKey="datos-personales"
      >
        <BaseFormPage
          FormComponent={PersonaFisicaForm}
          titleNew="Nueva Persona Física"
          titleEdit="Editar Persona Física"
          />
      </ContextTile> 
      <ContextTile
        title = "Documentos"
        tileKey = "documentos"
      >
      {isEdit && (<DocumentosPersona/>)}
      </ContextTile>  
    </ContextGrid>
  );
}
