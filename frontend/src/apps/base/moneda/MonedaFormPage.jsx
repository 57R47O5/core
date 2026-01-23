import BaseFormPage from "../../../components/forms/BaseFormPage";
import MonedaForm from "./MonedaForm";

export default function MonedaFormPage() {
  return (
    <BaseFormPage
      controller="moneda"
      FormComponent={MonedaForm}
      titleNew="Nuevo Moneda"
      titleEdit="Editar Moneda"
    />
  );
}
