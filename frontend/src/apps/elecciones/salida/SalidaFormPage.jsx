import BaseFormPage from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import VisitaFormPage from "../visita/VisitaFormPage";



export default function SalidaFormPage() {
  const {id } = useRouteMode();
  const controller = "salida";
  return (
    <InstanceProvider
      controller={controller} 
      id = {id}      
    >
      <ContextGrid
        defaultActive={0}
        columns={2}
      >
        <ContextTile
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
         title="Agregar visita" 
        >
          <VisitaFormPage>            
          </VisitaFormPage>
        </ContextTile>
      </ContextGrid>
    </InstanceProvider>
  );
}
