import BaseFormPage from "../../components/forms/BaseFormPage";
import PacienteForm from "./PacienteForm";

export default function PacienteFormPage() {
  return (
    <BaseFormPage
      controller="paciente"
      FormComponent={PacienteForm}
      titleNew="Nuevo Paciente"
      titleEdit="Editar Paciente"
    />
  );
}