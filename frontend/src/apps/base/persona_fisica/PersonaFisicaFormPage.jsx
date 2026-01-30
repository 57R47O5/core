import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";
import O2MInlineList from "../../../components/o2m/o2mInlineList";
import {DocumentoIdentidadSchema} from "../documento_identidad/DocumentoIdentidadForm";
import getAPIBase from "../../../api/BaseAPI";

export default function PersonaFisicaFormPage() {
  const controller = "persona-fisica"
  const {id} = getAPIBase(controller)
  return (
    <>
    <BaseFormPage
      controller = {controller}
      FormComponent={PersonaFisicaForm}
      titleNew="Nuevo Persona Fisica"
      titleEdit="Editar Persona Fisica"
      />  
      <O2MInlineList
        title="Documentos de identidad"
        columns={[
          { field: "tipo_id", label: "Tipo" },
          { field: "numero", label: "Número" },
        ]}
        filtros={{"persona__persona_fisica_id":id}}
        initialItem={{ tipo: "", numero: "" }}
        validationSchema={DocumentoIdentidadSchema}
        controller={"documento-identidad"}
      />    
    </>
  );
}
