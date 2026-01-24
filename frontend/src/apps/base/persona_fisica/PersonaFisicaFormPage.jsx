import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";

export default function PersonaFisicaFormPage() {
  return (
    <BaseFormPage
      controller="persona-fisica"
      FormComponent={PersonaFisicaForm}
      titleNew="Nuevo PersonaFisica"
      titleEdit="Editar PersonaFisica"
    />
  );
}
