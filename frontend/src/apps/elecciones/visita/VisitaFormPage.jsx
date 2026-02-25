import BaseFormPage from "../../../components/forms/BaseFormPage";
import VisitaForm from "./VisitaForm";

export default function VisitaFormPage() {
  return (
    <BaseFormPage
      controller="visita"
      FormComponent={VisitaForm}
      titleNew="Nuevo Visita"
      titleEdit="Editar Visita"
    />
  );
}
