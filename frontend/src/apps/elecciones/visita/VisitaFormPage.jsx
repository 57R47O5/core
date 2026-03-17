import BaseFormPage from "../../../components/forms/BaseFormPage";
import VisitaForm from "./VisitaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";


export default function VisitaFormPage() {
  return (
      <ContextGrid
        defaultActive={"base"}
        controller="visita"
      >
        <ContextTile
            title="Base"
            tileKey="base"
          >
          <BaseFormPage
            FormComponent={VisitaForm}
            titleNew="Nueva Visita"
            titleEdit="Editar Visita"
          />
        </ContextTile>
      </ContextGrid>
    );
}
