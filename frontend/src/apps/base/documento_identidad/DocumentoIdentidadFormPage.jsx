import BaseFormPage from "../../../components/forms/BaseFormPage";
import DocumentoIdentidadForm from "./DocumentoIdentidadForm";

export default function DocumentoIdentidadFormPage() {
  return (
    <BaseFormPage
      controller="documento-identidad"
      FormComponent={DocumentoIdentidadForm}
      titleNew="Nuevo DocumentoIdentidad"
      titleEdit="Editar DocumentoIdentidad"
    />
  );
}
