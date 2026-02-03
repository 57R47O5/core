import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaJuridicaForm from "./PersonaJuridicaForm";

export default function PersonaJuridicaFormPage() {
  return (
    <BaseFormPage
      controller="persona-juridica"
      FormComponent={PersonaJuridicaForm}
      titleNew="Nueva Persona Juridica"
      titleEdit="Editar Persona Juridica"
    />
  );
}
