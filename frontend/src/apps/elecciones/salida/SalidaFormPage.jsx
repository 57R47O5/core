import BaseFormPage, {BaseFormPageContent} from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import VisitaForm from "../visita/VisitaForm";
import { SiTiene } from "../../../components/displays/SiTiene";
import VisitaList from "../visita/VisitaList";

export function  SalidaFormPageContent({id, controller}) {
  const  {exists} = useInstance();

  return (
    <ContextGrid
      controller={"salida"}
      defaultActive={"salida"}
      columns={2}
    >
      <ContextTile
        tileKey="salida"
        title="Salida"
      >
    <BaseFormPage
      controller={controller}
      FormComponent={SalidaForm}
      titleNew="Nueva Salida"
      titleEdit="Editar Salida"
      />
      </ContextTile>        
      <ContextTile
        title={"Agregar Visita"}
        tileKey="agregar"
        capability={"agregar_visitas"}
      >
        <InstanceProvider
          controller={"visita"}
          id={null}
          defaults={{salida: id}}
        >
        <BaseFormPageContent
          id={null}
          isCreate = {true}
          controller="visita"
          FormComponent={VisitaForm}
          titleNew="Nueva Visita"
          titleEdit="Editar Visitas"
          />
        </InstanceProvider>
      </ContextTile>
        {(exists) ?  
        <ContextTile
            title={"Ver Visitas"}
            tileKey={"ver-visitas"}
          >  
          <VisitaList filters={{salida: id}}/>     
      </ContextTile>:<></>}
    </ContextGrid>
  )
}

export default function SalidaFormPage() {
  const { id } = useRouteMode();
  const controller = "salida";

  SalidaForm.initialValuesDefault = {
    fecha: new Date().toISOString().substring(0, 10),
    estado: 2,
  };

  VisitaForm.initialValuesDefault = {
    salida: id,
    resultado: 1,
  };

  return (
    <InstanceProvider
      controller={controller} 
      id = {id}      
    ><SalidaFormPageContent id={id} controller={controller}/>
    </InstanceProvider>
  );
}
