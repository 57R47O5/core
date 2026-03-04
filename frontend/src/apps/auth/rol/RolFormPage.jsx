import BaseFormPage from "../../../components/forms/BaseFormPage";
import RolForm from "./RolForm";

export default function RolFormPage() {
  return (
    <BaseFormPage
      controller="rol"
      FormComponent={RolForm}
      titleNew="Nuevo Rol"
      titleEdit="Editar Rol"
    />
  );
}
