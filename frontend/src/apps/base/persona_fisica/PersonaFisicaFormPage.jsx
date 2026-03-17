import { Spinner } from "react-bootstrap";
import BaseFormPage from "../../../components/forms/BaseFormPage";
import PersonaFisicaForm from "./PersonaFisicaForm";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import O2MProvider from "../../../components/o2m/O2MProvider";
import { useModelForm } from "../../../hooks/useModelForm";
import { documentoIdentidadFields } from "../documento_identidad/DocumentoIdentidadFields";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance } from "../../../context/InstanceContext";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";


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
        filtros={{persona_id: instance.persona_id }}
      />
    </O2MProvider>
  );
}


export default function PersonaFisicaFormPage() {
  const { isEdit } = useRouteMode();

  return (
    <ContextGrid
      defaultActive={"datos-personales"}
      controller={"persona-fisica"}
    > 
      <ContextTile
        title="Datos Personales"
        tileKey="datos-personales"
      >
        <BaseFormPage
          FormComponent={PersonaFisicaForm}
          titleNew="Nueva Persona Física"
          titleEdit="Editar Persona Física"
          />
      </ContextTile> 
      <ContextTile
        title = "Documentos"
        tileKey = "documentos"
      >
      {isEdit && (<DocumentosPersona/>)}
      </ContextTile>  
    </ContextGrid>
  );
}
