import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaJuridicaForm from "./PersonaJuridicaForm";

export default function PersonaJuridicaFormPage() {
  return (
    <BaseFormPage
      controller="persona-juridica"
      FormComponent={PersonaJuridicaForm}
      titleNew="Nuevo PersonaJuridica"
      titleEdit="Editar PersonaJuridica"
    />
  );
}
