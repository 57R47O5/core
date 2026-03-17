import BaseFormPage from "../../../components/forms/BaseFormPage";
import VotanteForm from "./VotanteForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";


export default function VotanteFormPage() {
  return (
      <ContextGrid
      defaultActive={"base"}
      controller="votante"
    >
      <ContextTile
          title="Base"
          tileKey="base"
        >
        <BaseFormPage
          FormComponent={VotanteForm}
          titleNew="Nuevo Votante"
          titleEdit="Editar Votante"
        />
      </ContextTile>
    </ContextGrid>
  );
}
