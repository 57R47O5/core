import { Spinner } from "react-bootstrap";
import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import O2MProvider from "../../../components/o2m/O2MProvider";
import { useModelForm } from "../../../hooks/useModelForm";
import { documentoIdentidadFields } from "../documento_identidad/DocumentoIdentidadFields";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";

function DocumentosPersona({}) {
  const { instance } = useInstance();

  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(documentoIdentidadFields);

  if (!instance)
    return (<Spinner/>)
  return (
    <O2MProvider
      controller="documento-identidad"
      columns={columns}
      initialItem={{
        ...initialValues,
        persona_id: instance.persona_id, 
      }}
      validationSchema={validationSchema}
    >
      <O2MInlineList
        title="Documentos de identidad"
        filtros={{persona_id: instance.persona_id }}
      />
    </O2MProvider>
  );
}


export default function PersonaFisicaFormPage() {
  const {id, isEdit } = useRouteMode();
  const controller = "persona-fisica";

  return (
    <>
      <BaseFormPage
        controller={controller}
        FormComponent={PersonaFisicaForm}
        titleNew="Nueva Persona Física"
        titleEdit="Editar Persona Física"
      />
      <InstanceProvider
        controller={controller}
        id = {isEdit && id}>
        {isEdit && (<DocumentosPersona/>)}
      </InstanceProvider>
    </>
  );
}
