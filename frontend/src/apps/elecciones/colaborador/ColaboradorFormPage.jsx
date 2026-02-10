import BaseFormPage from "../../../components/forms/BaseFormPage";
import ColaboradorForm from "./ColaboradorForm";

export default function ColaboradorFormPage() {
  return (
    <BaseFormPage
      controller="colaborador"
      FormComponent={ColaboradorForm}
      titleNew="Nuevo Colaborador"
      titleEdit="Editar Colaborador"
    />
  );
}
