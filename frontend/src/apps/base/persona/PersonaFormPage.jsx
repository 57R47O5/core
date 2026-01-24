import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaForm from "./PersonaForm";

export default function PersonaFormPage() {
  return (
    <BaseFormPage
      controller="persona"
      FormComponent={PersonaForm}
      titleNew="Nuevo Persona"
      titleEdit="Editar Persona"
    />
  );
}
