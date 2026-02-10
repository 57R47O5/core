import BaseFormPage from "../../../components/forms/BaseFormPage";
import CampanaForm from "./CampanaForm";

export default function CampanaFormPage() {
  return (
    <BaseFormPage
      controller="campana"
      FormComponent={CampanaForm}
      titleNew="Nuevo Campana"
      titleEdit="Editar Campana"
    />
  );
}
