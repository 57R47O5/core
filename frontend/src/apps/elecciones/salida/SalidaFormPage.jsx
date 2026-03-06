import BaseFormPage from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";

export default function SalidaFormPage() {
  return (
    <BaseFormPage
      controller="salida"
      FormComponent={SalidaForm}
      titleNew="Nueva Salida"
      titleEdit="Editar Salida"
    />
  );
}
