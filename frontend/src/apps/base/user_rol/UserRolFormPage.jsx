import BaseFormPage from "../../components/forms/BaseFormPage";
import UserRolForm from "./UserRolForm";

export default function UserRolFormPage() {
  return (
    <BaseFormPage
      controller="user-rol"
      FormComponent={UserRolForm}
      titleNew="Nuevo UserRol"
      titleEdit="Editar UserRol"
    />
  );
}
