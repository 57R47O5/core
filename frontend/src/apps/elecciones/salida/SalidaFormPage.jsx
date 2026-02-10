import BaseFormPage from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";

export default function SalidaFormPage() {
  return (
    <BaseFormPage
      controller="salida"
      FormComponent={SalidaForm}
      titleNew="Nuevo Salida"
      titleEdit="Editar Salida"
    />
  );
}
