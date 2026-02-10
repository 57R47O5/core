import BaseFormPage from "../../../components/forms/BaseFormPage";
import VotanteForm from "./VotanteForm";

export default function VotanteFormPage() {
  return (
    <BaseFormPage
      controller="votante"
      FormComponent={VotanteForm}
      titleNew="Nuevo Votante"
      titleEdit="Editar Votante"
    />
  );
}
