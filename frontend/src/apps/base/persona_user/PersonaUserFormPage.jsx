import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaUserForm from "./PersonaUserForm";

export default function PersonaUserFormPage() {
  return (
    <BaseFormPage
      controller="persona-user"
      FormComponent={PersonaUserForm}
      titleNew="Nuevo PersonaUser"
      titleEdit="Editar PersonaUser"
    />
  );
}
