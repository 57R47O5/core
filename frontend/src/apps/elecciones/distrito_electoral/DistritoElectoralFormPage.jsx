import BaseFormPage from "../../../components/forms/BaseFormPage";
import DistritoElectoralForm from "./DistritoElectoralForm";

export default function DistritoElectoralFormPage() {
  return (
    <BaseFormPage
      controller="distrito-electoral"
      FormComponent={DistritoElectoralForm}
      titleNew="Nuevo DistritoElectoral"
      titleEdit="Editar DistritoElectoral"
    />
  );
}
