import BaseFormPage from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { InstanceProvider } from "../../../context/InstanceContext";
import VisitaForm from "../visita/VisitaForm";
import VisitaList from "../visita/VisitaList";

export function  SalidaFormPageContent({id, controller}) {

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
        <BaseFormPage
          FormComponent={VisitaForm}
          />
        </InstanceProvider>
      </ContextTile>
      <ContextTile
            title={"Ver Visitas"}
            tileKey={"ver-visitas"}
            capability={"ver_visitas"}
          >  
          <VisitaList filters={{salida: id}}/>     
      </ContextTile>
      <ContextTile
        title={"Listar Visitas"}
        tileKey={"listar-visitas"}
        capability={"ver_visitas"}
      >
        <VisitaList filters={{salida: id}} mode={"lista"}/>
      </ContextTile>
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
