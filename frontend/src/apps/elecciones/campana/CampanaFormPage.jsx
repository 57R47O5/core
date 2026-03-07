import BaseFormPage from "../../../components/forms/BaseFormPage";
import CampanaForm from "./CampanaForm";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useRouteMode } from "../../../hooks/useRouteMode";

function Campana({}){
  const { instance } = useInstance();

  return <ContextGrid
      defaultActive={0}
        columns={2}
      >
    <ContextTile
      title={"Datos Campaña"}
    >
      <BaseFormPage
        controller="campana"
        FormComponent={CampanaForm}
        titleNew="Nueva Campaña Electoral"
        titleEdit="Editar Campaña Electoral"
      />
    </ContextTile>
  </ContextGrid>
}

export default function CampanaFormPage() {
  const {id} = useRouteMode();
  const controller = "campana"
  return (
      <InstanceProvider
        controller={controller} 
        id = {id}     
      >
        <Campana/>
        </InstanceProvider>
    );
}
