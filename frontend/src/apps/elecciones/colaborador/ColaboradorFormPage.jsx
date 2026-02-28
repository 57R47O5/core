import BaseFormPage from "../../../components/forms/BaseFormPage";
import ColaboradorForm from "./ColaboradorForm";
import { colaboradorActions } from "./colaboradorActions";

export default function ColaboradorFormPage() {
  return (
    <BaseFormPage
      controller="colaborador"
      FormComponent={ColaboradorForm}
      titleNew="Nuevo Colaborador"
      titleEdit="Editar Colaborador"
      extraActions={colaboradorActions}
    />
  );
}
