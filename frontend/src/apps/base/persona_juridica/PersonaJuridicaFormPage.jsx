import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaJuridicaForm from "./PersonaJuridicaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";

export default function PersonaJuridicaFormPage() {
  return (
        <ContextGrid
          defaultActive={"datos-personales"}
          controller={"persona-juridica"}
        >
          <ContextTile
              title="Datos Personales"
              tileKey="datos-personales"
            >
          <BaseFormPage
            FormComponent={PersonaJuridicaForm}
            titleNew="Nueva Persona Juridica"
            titleEdit="Editar Persona Juridica"
          />
          </ContextTile>
    </ContextGrid>
  );
}
