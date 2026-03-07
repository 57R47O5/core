import BaseFormPage from "../../../components/forms/BaseFormPage";
import SalidaForm from "./SalidaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import VisitaForm from "../visita/VisitaForm";
import BaseLink from "../../../components/displays/BaseLink";


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
  }
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
          title={"Agregar Visita"}
          >
          <BaseFormPage
            controller="visita"
            FormComponent={VisitaForm}
            titleNew="Nueva Visita"
            titleEdit="Editar Visita"
          />
        </ContextTile>
      </ContextGrid>
    </InstanceProvider>
  );
}
