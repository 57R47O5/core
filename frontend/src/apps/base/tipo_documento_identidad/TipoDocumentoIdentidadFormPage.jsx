import BaseFormPage from "../../../components/forms/BaseFormPage";
import TipoDocumentoIdentidadForm from "./TipoDocumentoIdentidadForm";

export default function TipoDocumentoIdentidadFormPage() {
  return (
    <BaseFormPage
      controller="tipo-documento-identidad"
      FormComponent={TipoDocumentoIdentidadForm}
      titleNew="Nuevo TipoDocumentoIdentidad"
      titleEdit="Editar TipoDocumentoIdentidad"
    />
  );
}
