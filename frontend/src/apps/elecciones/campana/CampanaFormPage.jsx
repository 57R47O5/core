import BaseFormPage from "../../../components/forms/BaseFormPage";
import CampanaForm from "./CampanaForm";

export default function CampanaFormPage() {
  return (
    <BaseFormPage
      controller="campana"
      FormComponent={CampanaForm}
      titleNew="Nueva Campaña Electoral"
      titleEdit="Editar Campaña Electoral"
    />
  );
}
