import BaseFormPage from "../../../components/forms/BaseFormPage";
import VisitaForm from "./VisitaForm";

export default function VisitaFormPage() {
  return (
    <BaseFormPage
      controller="visita"
      FormComponent={VisitaForm}
      titleNew="Nueva Visita"
      titleEdit="Editar Visita"
    />
  );
}
