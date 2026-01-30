import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import getAPIBase from "../../../api/BaseAPI";
import O2MProvider from "../../../components/o2m/O2MProvider";
import { useModelForm } from "../../../hooks/useModelForm"
import { documentoIdentidadFields } from "../documento_identidad/DocumentoIdentidadFields";

export default function PersonaFisicaFormPage() {
  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(documentoIdentidadFields);
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
      <O2MProvider
        controller={"documento-identidad"}
        columns={columns}
        initialItem={initialValues}
        validationSchema={validationSchema}
      >
        <O2MInlineList
          title="Documentos de identidad"
          filtros={{"persona__persona_fisica_id":id}}
        />    
      </O2MProvider>  
    </>
  );
}
