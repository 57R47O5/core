import BaseFormPage from "../../../components/forms/BaseFormPage";
import SeccionalForm from "./SeccionalForm";

export default function SeccionalFormPage() {
  return (
    <BaseFormPage
      controller="seccional"
      FormComponent={SeccionalForm}
      titleNew="Nuevo Seccional"
      titleEdit="Editar Seccional"
    />
  );
}
