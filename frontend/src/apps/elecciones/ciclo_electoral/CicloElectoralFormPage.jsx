import BaseFormPage from "../../../components/forms/BaseFormPage";
import CicloElectoralForm from "./CicloElectoralForm";

export default function CicloElectoralFormPage() {
  return (
    <BaseFormPage
      controller="ciclo-electoral"
      FormComponent={CicloElectoralForm}
      titleNew="Nuevo CicloElectoral"
      titleEdit="Editar CicloElectoral"
    />
  );
}
